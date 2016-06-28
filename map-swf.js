#!/usr/bin/env node

// Map ID
const mapArea = 33
const mapNo = 1

// RND is extract from 'Core.swf'
const RND = [3367, 28012, 6269, 26478, 24442, 27255, 28017, 3366, 6779, 7677, 7179, 28011, 24421, 27502, 3366, 7779, 24439, 27762, 6474, 7463, 28515, 3364, 6672, 28006, 27999, 27254, 7363, 6868]

// Procedure 1: Decode
let RND1 = []
;(function () {
  for (let rnd of RND) {
    rndstr = rnd > 10000 ? rnd.toString(16) : rnd.toString()
    RND1.push(rndstr.substr(0, 2))
    RND1.push(rndstr.substr(2, 4))
  }
})()
console.log("RND1", JSON.stringify(RND1))

// Procedure 2: Group
// Format: 33 a b c d 32 j k l
let kfile = []
;(function () {
  let area = 0, file = ''
  for (let rnd of RND1) {
    rnd = parseInt(rnd, 16)
    if (rnd < 90) {
      if (file !== '') {
        area = parseInt(area.toString(16))
        kfile.push([area, file])
        file = ''
      }
      area = rnd
    } else {
      file += String.fromCharCode(rnd)  // 91=a, 92=b, ...
    }
  }
  kfile.push([area, file])  // Seems last item needn't to convert
})()
console.log("kfile", JSON.stringify(kfile))

// Procedure 3: Find
// Find No.`mapNo` of `kfile[i][0] == areaID`, and its file name is `kfile[i][1]`
;(function () {
  let i = 0
  for (let _ of kfile) {
    let area = _[0], file = _[1]
    if (area === mapArea) {
      i += 1
      if (i === mapNo)
        console.log(`${mapArea}-${mapNo}: ${file}`)
    }
  }
})()
