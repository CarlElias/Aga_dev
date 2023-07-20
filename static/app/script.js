const swiperEl = document.querySelector('swiper-container');

swiperEl.addEventListener('progress', (event) => {
    const [swiper, progress] = event.detail;
});

swiperEl.addEventListener('slidechange', (event) => {
    console.log('slide changed');
});


const swiperParams = {
    breakpoints: {
        760: {
            slidesPerView: 3,
        },
        640: {
            slidesPerView: 1,
        },
    },
    on: {
        init() {
            slidesPerView: 3
        },
    },
};

// now we need to assign all parameters to Swiper element
Object.assign(swiperEl, swiperParams);

const swiperElLisfestyle = document.getElementById('swiper-lifestyle');

swiperElLisfestyle.addEventListener('progress', (event) => {
    const [swiper, progress] = event.detail;
});

swiperElLisfestyle.addEventListener('slidechange', (event) => {
    console.log('slide changed');
});

const swiperParamsLyfestyle = {
    breakpoints: {
        760: {
            slidesPerView: 1,
        },
        1024: {
            slidesPerView: 2,
        },

    },
    on: {
        init() {
            slidesPerView: 2
        },
    },
};

Object.assign(swiperElLisfestyle, swiperParamsLyfestyle);

// and now initialize it
// swiperElLisfestyle.initialize();


const swiperChain = document.getElementById('swiperall')

swiperChain.addEventListener('progress', (event) => {
    const [swiper, progress] = event.detail;
});

swiperChain.addEventListener('slidechange', (event) => {
    console.log('slide changed');
});


const swiperChainParams = {
    breakpoints: {
        760: {
            slidesPerView: 3,
        },
        640: {
            slidesPerView: 1,
        },
    },
    on: {
        init() {
            slidesPerView: 3
        },
    },
};

Object.assign(swiperChain, swiperChainParams);
// swiperChain.initialize();