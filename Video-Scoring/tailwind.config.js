/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  content: [],
  theme: {
    extend: {

      backgroundImage: {
        'dark-gradient': 'linear-gradient(135deg, #000000, #111111, #222222, #333333, #444444, #555555)',
      },

      clipPath: {
        'ellipse': 'ellipse(90px 30px at 100px 50px)'

      },  

      boxShadow: {
        glow: '0 0 1px 0px #ff9a00, 0 0 20px 0px #ff6a00, 0 0 30px 0px #ff4500',
      },
      keyframes: {
        glow: {
          '0%': { boxShadow: '0 0 0px 0px #577399, 0 0 30px 2px #f3ec78, 0 0 30px 2px #af4261' },
          '100%': { boxShadow: '0 0 0px 0px #00c9a7, 0 0 30px 9px #ff6a88 , 0 0 30px 15px #4d9de0 ' },        },
      },
      animation: {
        glow: 'glow 2s infinite alternate',
      },
    },
  },
  plugins: [
      function ({ addUtilities }) {
        addUtilities({
          '.clip-ellipse': {
            'clip-path': 'ellipse(90px 30px at 100px 50px)',
          },
        });
      },
    ],
}

