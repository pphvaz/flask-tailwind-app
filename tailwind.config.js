module.exports = {
    content: [
      './templates/**/*.html', // HTML templates
      './static/js/*.js',      // JS files
    ],
    theme: {
      extend: {
        colors: {
          azul: {
            escura: '#100753',
            forms: '#190D6D',
            input: 'rgba(25, 13, 109, 0.2)',
            darkblue: '#0B0534',
          },
        },
        fontFamily: {
          varta: ['Varta', 'sans-serif'],
        },
        animation: {
          shake: 'shake 0.5s ease-in-out infinite',
        },
        keyframes: {
          shake: {
            '0%, 100%': { transform: 'translateX(0)' },
            '25%': { transform: 'translateX(-2px)' },
            '50%': { transform: 'translateX(2px)' },
            '75%': { transform: 'translateX(-2px)' },
          },
        },
      },
    },
    plugins: [],
  };
  