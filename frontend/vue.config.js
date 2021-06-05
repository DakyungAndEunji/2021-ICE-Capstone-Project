module.exports = {
  transpileDependencies: ["vuetify"],
  publicPath: "/",
  devServer: {
    // proxy: {
    //   "/api": {
    //     target: "http://localhost:5000",
    //     changeOrigin: true,
    //   },
    // },
  },

  pluginOptions: {
    cordovaPath: "src-cordova",
  },
};
