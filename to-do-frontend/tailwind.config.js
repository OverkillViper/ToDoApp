/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{vue,js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                primary: "#181820",
                secondary: "#21212b",
                ternary: "#fbe6a2",
                accent: "#9c82f7",
                secondary2: "#2d2d3b"
            },
            fontFamily: {
                primary: ["CriqueGrotesk-Medium"],
                bd:      ["CriqueGrotesk-Bold"],
                black:   ["CriqueGrotesk-Black"],
                normal:  ["CriqueGrotesk"]
            }
        },
    },
    plugins: [],
}