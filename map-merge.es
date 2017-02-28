import { promisify, promisifyAll } from 'bluebird'
import _ from 'lodash'
import fs from 'fs'
import libxmljs from 'libxmljs'
import path from 'path'
import childProcess from 'child_process'
const execAsync = promisify(childProcess.exec)
promisifyAll(fs)

function getSymbolClass(xml) {
  const results = {}
  const scs = xml.find(`/swf/tags/item[@type='SymbolClassTag']`)
  for (const sc of scs) {
    const tags  = sc.find( 'tags/item').map(node => node.text())
    const names = sc.find('names/item').map(node => node.text())
    for (const [tag, name] of _.zip(tags, names)) {
      results[tag] = name
    }
    if (tags.length !== names.length) {
      console.error('getSymbolClass', '`tags` and `names` length not equal!')
      process.exit(1)
    }
  }
  return results
}

function getExtraNode(id, childId) {
  const xml = libxmljs.parseXml(`
    <item characterId="${childId}" clipDepth="0" depth="${id}" name="extra${id}" placeFlagHasCharacter="true" placeFlagHasClipActions="false" placeFlagHasClipDepth="false" placeFlagHasColorTransform="false" placeFlagHasMatrix="true" placeFlagHasName="true" placeFlagHasRatio="false" placeFlagMove="false" ratio="0" type="PlaceObject2Tag">
      <matrix hasRotate="false" hasScale="false" nRotateBits="0" nScaleBits="0" nTranslateBits="15" rotateSkew0="0" rotateSkew1="0" scaleX="0" scaleY="0" translateX="0" translateY="0" type="MATRIX"/>
    </item>
  `)
  return xml.root()
}

(async () => {
  const argv = process.argv.slice(process.argv[1].endsWith('.js') ? 2 : 1)
  const files = argv.slice(0).map(s => path.parse(s).name)

  // Convert SWF to XML
  console.log('Converting', files)
  const xmls = []
  await Promise.all(files.map(async(name, i) => {
    const swfFile = `${name}.swf`
    const xmlFile = `${name}.xml`
    await execAsync(`ffdec -swf2xml "${swfFile}" "${xmlFile}"`)
    const dat = await fs.readFileAsync(xmlFile)
    xmls[i] = libxmljs.parseXml(dat)
  }))
  if (xmls.length < 2) {
    console.error(`XML number incorrect!`)
    process.exit(1)
  }
  const [ mainXML, ...spsXML ] = xmls

  // Prepare env
  const mainCnt = mainXML.get(`/swf/tags`)
  const mainSC  = getSymbolClass(mainXML)
  const mapId  = _.findKey(mainSC, (n) => n.endsWith('.map_1'))
  const map    = mainCnt.get(`item[@spriteId='${mapId}']`)
  const mapCnt = map.get('subTags')

  // Remove ShowFrameTag
  const mapSFT = mapCnt.get(`item[@type='ShowFrameTag']`)
  mapSFT.remove()

  // Process merging
  const idTags = ['characterId', 'characterID', 'shapeId', 'spriteId', 'bitmapId']
  spsXML.map((spXML, i) => {
    console.log(`Merging`, i)
    const idBase = (i + 1) * 1000
    const spCnt  = spXML.get(`/swf/tags`)

    // Merge SP map to MAP as extra
    const spSC  = getSymbolClass(spXML)
    const spId  = _.findKey(spSC, (n) => n.startsWith('scene.sally.mc.MCCellSP'))
    const spRef = getExtraNode(idBase, idBase + Number(spId))
    mapCnt.addChild(spRef)

    // Replace ID
    for (const tag of idTags) {
      const items = spXML.find(`//item[@${tag}]`)
      for (const item of items) {
        const ida = item.attr(tag)
        const nid = idBase + Number(ida.value())
        ida.value(nid <= 65535 ? nid : 65535)
      }
    }
    // Merge SP elements to main XML
    for (const tag of idTags) {
      const items = spCnt.find(`item[@${tag}]`)
      for (const item of items) {
        mainCnt.addChild(item)
      }
    }
  })

  // Add ShowFrameTag
  mapCnt.addChild(mapSFT)

  // Save & Convert XML to SWF
  const fname = `${files[0]}_merge`
  console.log('Converting', fname)
  await fs.writeFileAsync(`${fname}.xml`, mainXML.toString())
  await execAsync(`ffdec -xml2swf "${fname}.xml" "${fname}.swf"`)
})()