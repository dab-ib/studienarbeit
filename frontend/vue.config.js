module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer:{
    port: '8080',
    host: 'dabib.hopto.org',
    proxy: process.env.VUE_APP_BACKEND_URL

  }
}
