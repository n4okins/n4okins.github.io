"use client";
import ContentPage from "@/pages/render"
import React, { useState } from "react"

export default function Home() {
  const [lang, setLang] = useState("ja");
  return (
    <div className="text-wrap dark:bg-gray-700">
      <div className="flex justify-end mt-2">
        <button
          onClick={() => setLang('ja')}
          className={`w-32 py-2 text-md dark:text-white ${lang === 'ja' ? 'bg-dark-200 ' : 'bg-dark-200 hover:bg-white dark:hover:bg-gray-500'} transition-colors duration-300`}
        >
          {lang === "ja" ? "日本語" : "Japanese"}
        </button>
        <button
          onClick={() => setLang('en')}
          className={`w-32 py-2 text-md dark:text-white ${lang === 'ja' ? 'bg-dark-200 hover:bg-white dark:hover:bg-gray-500' : 'bg-dark-800'} transition-colors duration-300`}
        >
          {lang === "ja" ? "英語" : "English"}
        </button>
      </div>
      <ContentPage lang={lang.toString()} />
    </div>
  )
}