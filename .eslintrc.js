module.exports = {
  'env': {
    'es6': true,
    'node': true,
  },
  'extends': [
    'eslint:recommended',
    'plugin:import/errors',
    'plugin:import/warnings',
  ],
  'installedESLint': true,
  'parser': 'babel-eslint',
  'plugins': [
    'import',
  ],
  'rules': {
    'comma-dangle': ['error', 'always-multiline'],
    'indent': ['warn', 2],
    'linebreak-style': ['error', 'unix'],
    'no-console': 'off',
    'no-var': 'error',
    'no-unused-vars': ['warn', {'args': 'none'}],
    'semi': ['error', 'never'],
    'unicode-bom': 'error',
  },
  'settings': {
    'import/resolver': {
      'node': {
        'extensions': ['.es', '.js'],
        'paths': [__dirname],
      },
    },
    'import/core-modules': [
    ],
  },
}
