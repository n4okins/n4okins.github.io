import Link from 'next/link'

export default function content(lang: string) {
    return (
        {
            "ja": {
                "name": "志子田 直輝（しこだ なおき）",
                "affiliation": "奈良先端科学技術大学院大学 先端科学技術研究科 先端科学技術専攻 情報科学領域 博士前期課程 1年",
                "interested_in": {
                    "title": "自己紹介",
                    "content": <p>奈良にいます。
                        機械学習に興味があります。特に自然言語処理、画像処理、グラフニューラルネットワークに関心があります。
                        セキュリティにも興味があります。低レイヤーはあまり詳しくないですが、少しずつ学んでいます。
                        Pythonをメインに、いろんなプログラミング言語をかじりながら過ごしています。
                        英語は得意ではないですが、講義も研究室も英語ばかりなので絶賛実践形式で勉強中です。
                        <br />
                        お酒は量は飲めませんが、最近はウイスキーが好きです。
                    </p>
                },
                "background": {
                    "title": "略歴",
                    "content": [
                        {
                            "td": "現在",
                            "content": [
                                "情報科学領域",
                                <Link href='https://nlp.naist.jp/ja/' target='_blank' className='mx-2 text-blue-400 hover:text-blue-200' key="link" >
                                    自然言語処理学研究室（渡辺研究室）
                                </Link>,
                                "所属 博士前期課程 1年"
                            ]
                        },
                        {
                            "td": "2024.04",
                            "content": "奈良先端科学技術大学院大学 先端科学技術研究科 先端科学技術専攻 入学"
                        },
                        {
                            "td": "2024.03",
                            "content": "東京都市大学 情報工学部 知能情報工学科 卒業"
                        },
                        {
                            "td": " | ",
                            "content": [
                                "同学科",
                                <Link href='https://www.ke.tcu.ac.jp/labo/is07/' target='_blank' className='mx-2 text-blue-400 hover:text-blue-200' key="link">
                                    神野研究室
                                </Link>,
                                "所属"
                            ]
                        },
                        {
                            "td": "2020.04",
                            "content": "東京都市大学 情報工学部 知能情報工学科 入学"
                        }
                    ]
                },
                "internship": {
                    "title": "インターンシップ",
                    "content": [
                        {
                            "td": "2022.10 - 現在",
                            "content": [
                                <Link href="https://nnn.ed.jp/recruit/special/intern/" key="link" target="_blank" className="text-blue-400 hover:text-blue-200">
                                    角川ドワンゴ学園 N Code Labo
                                </Link>,
                                "講師"
                            ]
                        },
                        {
                            "td": "2022.04 - 2022.10",
                            "content": [
                                <Link href="https://nnn.ed.jp/recruit/special/intern/" key="link" target="_blank" className="text-blue-400 hover:text-blue-200">
                                    角川ドワンゴ学園 N/S高校
                                </Link>,
                                "プログラミングTA"
                            ]
                        }
                    ]
                },
                "other": {
                    "title": "その他",
                    "content": [
                        [
                            <Link href="https://www.security-camp.or.jp/minicamp/online2021.html" key="link" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">
                                セキュリティ・ミニキャンプ オンライン 2021
                            </Link>,
                            "修了"
                        ],
                        [
                            <Link href="https://www.ipa.go.jp/jinzai/security-camp/2022/zenkoku/index.html" key="link" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">
                                セキュリティ・キャンプ全国大会 オンライン 2022
                            </Link>, "AIセキュリティコース（Dコース）修了"
                        ]
                    ]
                },
                "publication": {
                    "title": "発表等",
                    "content": [
                        {
                            "td": "2023.08",
                            "content": [
                                "データ構造としてのグラフ構造の検討",
                                <Link href="https://sites.google.com/shibaura-it.ac.jp/nonlinear-summer/ホーム" key="link" target="_blank" className="text-blue-400 hover:text-blue-200">
                                    非線形ワークショップ 夏の大会＠ホテル光風閣くわるび （ポスター発表）
                                </Link>,
                            ]
                        },
                        {
                            "td": "2022.12",
                            "content": [
                                "グラフニューラルネットワークの画像処理への適用に関する検討",
                                <Link href="http://www.hisenkei.net/NLWS/20221217.html" target="_blank" key="link" className="text-blue-400 hover:text-blue-200">
                                    非線形ワークショップ＠芝浦工業大学 （ポスター発表）
                                </Link>,
                            ]
                        }
                    ]
                },
                "certification": {
                    "title": "資格",
                    "content": [
                        { "td": "現在勉強中", "content": "情報処理安全確保支援士試験" },
                        { "td": "現在勉強中", "content": "TOEIC L&R", "className": "border-b border-gray-700 dark:border-gray-100" },
                        { "td": "2024.03", "content": "学士（工学）" },
                        { "td": "2023.04", "content": "TOEIC L&R 665" },
                        {
                            "td": "2022.06", "content": <Link href="https://www.ipa.go.jp/shiken/kubun/ap.html" target="_blank">
                                応用情報技術者
                            </Link>
                        },
                        {
                            "td": "2021.05", "content": <Link href="https://www.ipa.go.jp/shiken/kubun/ip.html" target="_blank">
                                ITパスポート
                            </Link >
                        },
                        { "td": "その他", "content": "漢字検定2級, 世界遺産検定2級など", "className": "bg-gray-300 dark:bg-gray-700" },
                    ]
                },
                "updated": "2024年4月26日更新"
            },
            "en": {
                "name": "Naoki Shikoda",
                "affiliation": "First-year master's student at NAra Institute of Science and Technology, NAIST",
                "interested_in": {
                    "title": "About Me",
                    "content": <p>
                        I am currently studying in Nara.
                        I am interested in machine learning, especially natural language processing, image processing, and graph neural networks.
                        I am also interested in security. I&apos;m not very knowledgeble about lower layers yet, but I&apos;m learning little by little.

                        I mainly use Python, dabbling in various programming languages.

                        I&apos;m not good at English, but since all my lectures and research are in English, I&apos;m studying it in a practical way.
                        <br />
                        I&apos;m not a big drinker, but I&apos;ve recently taken a liking to whiskey.
                    </p>
                },
                "background": {
                    "title": "Background",
                    "content": [
                        {
                            "td": "Current",
                            "content": [
                                "Member of the ",
                                <Link href="https://nlp.naist.jp/en/" target="_blank" key="link" className="mx-2 text-blue-400 hover:text-blue-200">
                                    Natural Language Processing Laboratory (Watanabe Lab)
                                </Link>,
                                "First year of the master's program"
                            ]
                        },
                        {
                            "td": "April 2024",
                            "content": "Enrolled in the Graduate School of Advanced Science and Technology, Nara Institute of Science and Technology"
                        },
                        {
                            "td": "March 2024",
                            "content": "Graduated from Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering"
                        },
                        {
                            "td": " | ",
                            "content": [
                                "Member of the ",
                                <Link href='https://www.ke.tcu.ac.jp/labo/is07/' target='_blank' key="link" className='mx-2 text-blue-400 hover:text-blue-200'>
                                    Jinno Lab
                                </Link>,
                                "at the same department"
                            ]
                        },
                        {
                            "td": "April 2020",
                            "content": "Enrolled in Tokyo City University, Faculty of Information Engineering, Department of Intelligent Information Engineering"
                        }
                    ]
                },
                "internship": {
                    "title": "Internships",
                    "content": [
                        {
                            "td": "October 2022 - Present",
                            "content": [
                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" key="link" className="text-blue-400 hover:text-blue-200">
                                    KADOKAWA DWANGO Educational Institute N Code Labo
                                </Link>,
                                "Instructor"
                            ]
                        },
                        {
                            "td": "April 2022 - October 2022",
                            "content": [
                                <Link href="https://nnn.ed.jp/recruit/special/intern/" target="_blank" key="link" className="text-blue-400 hover:text-blue-200">
                                    KADOKAWA DWANGO Educational Institute N/S High School
                                </Link>,
                                "Programming Teaching Assistant"
                            ]
                        }
                    ]
                },
                "other": {
                    "title": "Other",
                    "content": [
                        [
                            <Link href="https://www.security-camp.or.jp/minicamp/online2021.html" target="_blank" key="link" className="mr-4 text-blue-400 hover:text-blue-200">
                                Security Mini Camp Online 2021
                            </Link>,
                            "Completed"
                        ],
                        [
                            <Link href="https://www.ipa.go.jp/jinzai/security-camp/2022/zenkoku/index.html" key="link" target="_blank" className="mr-4 text-blue-400 hover:text-blue-200">
                                Security Camp Online 2022
                            </Link>, "Comleted AI Security Course (D Course)"
                        ]
                    ]
                },
                "publication": {
                    "title": "Publications",
                    "content": [
                        {
                            "td": "2023.08",
                            "content": [
                                "データ構造としてのグラフ構造の検討 ",
                                <Link href="https://sites.google.com/shibaura-it.ac.jp/nonlinear-summer/ホーム" key="link" target="_blank" className="text-blue-400 hover:text-blue-200">
                                    Non Linear Workshop ＠ Hotel Kuwarubi （poster）
                                </Link>,
                            ]
                        },
                        {
                            "td": "2022.12",
                            "content": [
                                "グラフニューラルネットワークの画像処理への適用に関する検討",
                                <Link href="http://www.hisenkei.net/NLWS/20221217.html" target="_blank" key="link" className="text-blue-400 hover:text-blue-200">
                                    Non Linear Workshop ＠Shibaura Institute of technology （poster）
                                </Link>,
                            ]
                        }
                    ]
                },
                "certification": {
                    "title": "Certifications",
                    "content": [
                        { "td": "Currently Studying", "content": "Information Processing Security Support Technician Examination" },
                        { "td": "Currently Studying", "content": "TOEIC L&R", "className": "border-b border-gray-700 dark:border-gray-100" },
                        { "td": "March 2024", "content": "Degree in Engineering" },
                        { "td": "April 2023", "content": "TOEIC L&R 665" },
                        {
                            "td": "June 2022", "content": <Link href="https://www.ipa.go.jp/shiken/kubun/ap.html" key="link" target="_blank">
                                Applied Information Technology Engineer
                            </Link>
                        },
                        {
                            "td": "May 2021", "content": <Link href="https://www.ipa.go.jp/shiken/kubun/ip.html" key="link" target="_blank">
                                IT Passport
                            </Link >
                        },
                        { "td": "その他", "content": "Kanji proficiency test, World Heritage test, etc", "className": "bg-gray-300 dark:bg-gray-700" },
                    ]
                },
                "updated": "Updated April 26, 2024"
            },
        }[lang]
    )
}