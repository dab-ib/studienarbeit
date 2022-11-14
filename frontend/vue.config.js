module.exports = {
  "transpileDependencies": [
    "vuetify"
  ],
  devServer:{
    port: '8080',
    host: 'dabib.tech',
    proxy: process.env.VUE_APP_BACKEND_URL

  }
}
