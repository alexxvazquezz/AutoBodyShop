const path = require('path');

module.exports = {
  entry: './static/bundles/bundle.jsx',
  output: {
    filename: 'bundle.js',
    path: path.resolve(__dirname, 'static/bundles'),
  },
  module: {
    rules: [
      {
        test: /\.jsx?$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env', '@babel/preset-react'],
          },
        },
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.jsx'],
  },
};
