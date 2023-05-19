module.exports = {
    "transpileDependencies": [
        "vuetify"
    ],
    devServer: {
        port: '8080',
        host: 'localhost',
        proxy: process.env.VUE_APP_BACKEND_URL

    }
}
