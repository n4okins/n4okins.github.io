/** @type {import('tailwindcss').Config} */
module.exports = {
    extend: {
        wordBreak: {
          'keep-all': 'keep-all',
        }
      },
    content: [
        "./app/**/*.{js,ts,jsx,tsx,mdx}",
        "./pages/**/*.{js,ts,jsx,tsx,mdx}",
        "./components/**/*.{js,ts,jsx,tsx,mdx}",

        // Or if using `src` directory:
        "./src/**/*.{js,ts,jsx,tsx,mdx}",
    ],
    theme: {
        extend: {
            
        },
    },
    plugins: [],
}