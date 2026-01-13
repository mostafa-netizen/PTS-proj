/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Industrial color scheme
        industrial: {
          50: '#f5f7fa',
          100: '#eaeef4',
          200: '#d0dae6',
          300: '#a8bbd1',
          400: '#7896b8',
          500: '#5778a0',
          600: '#445f85',
          700: '#384d6d',
          800: '#31425c',
          900: '#2c394e',
          950: '#1d2534',
        },
        steel: {
          50: '#f6f7f9',
          100: '#eceef2',
          200: '#d5dae2',
          300: '#b0bac9',
          400: '#8595ab',
          500: '#677891',
          600: '#526078',
          700: '#434e62',
          800: '#3a4353',
          900: '#343a47',
          950: '#23272f',
        }
      }
    },
  },
  plugins: [],
}

