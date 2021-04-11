var merge = require('webpack-merge');
var webpack = require('webpack');
var CopyWebpackPlugin = require('copy-webpack-plugin');
var MiniCssExtractPlugin = require('mini-css-extract-plugin');
var OptimizeCSSAssetsPlugin = require('optimize-css-assets-webpack-plugin');
var UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const path = require('path');

var common = {
  watchOptions: {
    poll: (process.env.WEBPACK_WATCHER_POLL || 'true') === 'true'
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: [/node_modules/],
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: [/\.scss$/, /\.css$/],
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'postcss-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(png|jpg|gif|svg)$/,
        exclude: /fonts/,
        loader: 'file-loader?name=/images/[name].[ext]'
      },
      {
        test: /\.(ttf|eot|svg|woff2?)$/,
        exclude: /images/,
        use: [{
          loader: 'file-loader',
          options: {
            name: '[name].[ext]',
            outputPath: 'fonts/',
            publicPath: '../fonts'
          }
        }]
      }
    ]
  },
  optimization: {
    minimizer: [
      new UglifyJsPlugin({cache: true, parallel: true}),
      new OptimizeCSSAssetsPlugin({})
    ]
  }
};

module.exports = [
  merge(common, {
    entry: [
      __dirname + '/app/app.scss',
      path.resolve(__dirname + '/app/app.js')
    ],
    output: {
      path: path.resolve(__dirname + '/../public'),
      filename: 'js/app.js'
    },
    resolve: {
      modules: [
        path.resolve(__dirname + '/node_modules'),
        path.resolve(__dirname + '/app')
      ]
    },
    plugins: [
      new CopyWebpackPlugin([{from: path.resolve(__dirname + '/static')}]),
      new MiniCssExtractPlugin({filename: 'css/app.css'}),
      new webpack.ProvidePlugin({$: 'jquery', jQuery: 'jquery'}),
      new webpack.ProvidePlugin({ moment: "moment" }),
    ]
  })
];
