/**
 * @author liumengniu
 * @Date: 2021-7-3
 */

const path = require("path");
const webpack = require("webpack");

module.exports = {
  devServer: {
    port: 5050
  },
  webpack: {
    publicPath: "./",
    configure: (webpackConfig, {env, paths}) => {
      webpackConfig.resolve.fallback = {
        "buffer": require.resolve("buffer")
      };
      webpackConfig.module.rules.push(
        {
          test: /\.m?js$/,
          resolve: {
            fullySpecified: false
          },
        }),
      webpackConfig.ignoreWarnings = [/Failed to parse source map/];
      return webpackConfig;
    },
    alias: {
      "@": path.resolve("src"),
      "@statics": path.resolve(__dirname, "src/statics"),
      "@views": path.resolve(__dirname, "src/views"),
      "@comp": path.resolve(__dirname, "src/components"),
      "@services": path.resolve(__dirname, "src/services"),
      "@utils": path.resolve(__dirname, "src/utils"),
      "@redux": path.resolve(__dirname, "src/redux"),
      "@styles": path.resolve(__dirname, "src/styles")
    },
    plugins: [
      new webpack.ProvidePlugin({
        process: "process/browser",
        Buffer: ["buffer", "Buffer"],
      }),
    ]
  },
  eslint: {
    enable: false,
  },
};
