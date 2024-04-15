import Link from "next/link";
import styles from "./page.module.css";

export default function Home() {
  return (
    <main className={styles.main}>
      <h1 className={styles.title}>こんにちは！</h1>
      <p>
        志子田 直輝（しこだ なおき）です。
        奈良先端科学技術大学院大学（NAIST）の
        <Link href="https://nlp.naist.jp/" rel="noopener noreferrer" target="_blank">
          <a>自然言語処理学研究室</a>
        </Link>の修士1年です。
      </p>
    </main>
  );
}
