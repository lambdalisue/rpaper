import path from 'path';
import webpack from 'webpack';
import ExtractTextPlugin from 'extract-text-webpack-plugin';

const DEBUG = !process.argv.includes('--release');
const VERBOSE = process.argv.includes('--verbose');


export default {
  cache: DEBUG,
  debug: DEBUG,
  target: 'web',
  devtool: DEBUG ? 'inline-source-map' : false,

  stats: {
    colors: true,
    reasons: DEBUG,
    hash: VERBOSE,
    version: VERBOSE,
    timings: true,
    chunks: VERBOSE,
    chunkModules: VERBOSE,
    cached: VERBOSE,
    cachedAssets: VERBOSE,
  },

  entry: {
    'common': [
      'babel-polyfill',
      'array-includes/shim',
    ],

    'reservations': [
      'ts/views/reservations',
    ],
  },

  output: {
    publicPath: '/static/',
    sourcePrefix: '  ',
    path: path.join(__dirname, 'static/static'),
    filename: 'js/[name].js',
    sourceMapFilename: '[file].map',
  },

  resolve: {
    root: [
      path.join(__dirname, 'src/frontend'),
    ],
    extensions: ['', '.js', '.ts', '.tag', '.css', '.less'],
  },

  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /node_modules/,
        loader: 'babel'
      },
      {
        test: /\.ts$/,
        exclude: /node_modules/,
        loader: 'babel!ts'
      },
      {
        test: /\.tag$/,
        exclude: /node_modules/,
        loader: 'babel!riotjs?type=babel',
      },
      {
        test: /\.css$/,
        exclude: /node_modules/,
        loader: ExtractTextPlugin.extract('style', 'css'),
      },
      {
        test: /\.less$/,
        exclude: /node_modules/,
        loader: ExtractTextPlugin.extract('style', 'css!less'),
      },
      {
        test: /\.(png|svg|jpg)(\?[a-z0-9=\.]+)?$/,
        exclude: /node_modules/,
        loader: 'url-loader?limit=100000&publicPath=../&name=img/[hash].[ext]'
      },
      {
        test: /\.(woff2?|eot|ttf)(\?[a-z0-9=\.]+)?$/,
        exclude: /node_modules/,
        loader: 'url-loader?limit=100000&publicPath=../&name=font/[hash].[ext]'
      },
    ]
  },

  plugins: [
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.optimize.CommonsChunkPlugin('common', 'js/common.js'),
    new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /ja/),
    new webpack.ProvidePlugin({
      riot: 'riot',
    }),
    new ExtractTextPlugin('css/[name].css'),
  ],
};
