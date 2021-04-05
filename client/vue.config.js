module.exports = {
    css: {
        loaderOptions: {
            sass: {
                prependData: `
          @import "@/assets/colors.scss";
        `,
            },
        },
    },
};