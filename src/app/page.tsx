"use client";
import Japanese from "@/pages/ja"
import English from "@/pages/en"
import React, { useState } from "react"

export default function Home() {
  const [lang, setLang] = useState("ja");
  return (
    <div className="container text-wrap">
      <div className="flex justify-end mt-2">
        <button
          onClick={() => setLang('ja')}
          className={`w-32 py-2 text-sm ${lang === 'ja' ? 'text-white bg-dark-900' : 'text-dark-200 hover:bg-gray-300'} transition-colors duration-300`}
        >
          {lang === "ja" ? "日本語" : "Japanese"}
        </button>
        <button
          onClick={() => setLang('en')}
          className={`w-32 py-2 text-sm ${lang === 'ja' ? 'text-white bg-dark-200 hover:bg-gray-300' : 'text-dark-200 bg-dark-900'} transition-colors duration-300`}
        >
          {lang === "ja" ? "英語" : "English"}
        </button>
      </div>
      {lang === "ja" ? <Japanese /> : <English />}
    </div>
  )
}