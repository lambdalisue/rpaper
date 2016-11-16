import path from 'path';
import webpack from 'webpack';
import ExtractTextPlugin from 'extract-text-webpack-plugin';

const DEBUG = !process.argv.includes('--release');
const VERBOSE = process.argv.includes('--verbose');


export default {
  cache: DEBUG,
  debug: DEBUG,
  target: 'web',
  devtool: DEBUG ? 'source-map' : false,

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
      'whatwg-fetch',
    ],

    'instrument': [
      'js/main',
      'js/views/instrument',
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
    modulesDirectories: [
      path.join(__dirname, 'node_modules'),
      path.join(__dirname, 'src/frontend'),
    ],
    extensions: ['', '.js', '.tag', '.css', '.less'],
  },

  module: {
    loaders: [
      {
        test: /\.js$/,
        loader: 'babel'
      },
      {
        test: /\.tag$/,
        exclude: /node_modules/,
        loader: 'babel!riotjs?type=babel',
      },
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract(
          'style',
          'css'
        ),
      },
      {
        test: /\.less$/,
        loader: ExtractTextPlugin.extract(
          'style',
          'css!less'
        ),
      },
      {
        test: /\.(png|svg|jpg)(\?[a-z0-9=\.]+)?$/,
        loader: 'url-loader?limit=100000&publicPath=../&name=img/[hash].[ext]'
      },
      {
        test: /\.(woff2?|eot|ttf)(\?[a-z0-9=\.]+)?$/,
        loader: 'url-loader?limit=100000&publicPath=../&name=font/[hash].[ext]'
      },
    ]
  },

  plugins: [
    new ExtractTextPlugin('css/[name].css'),
    new webpack.ProvidePlugin({
      riot: 'riot',
    }),
    new webpack.optimize.OccurenceOrderPlugin(),
    new webpack.ContextReplacementPlugin(
      /moment[\/\\]locale$/, /ja/
    ),
  ],
};
