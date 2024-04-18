// components/LanguageSwitcher.tsx
import { useRouter } from 'next/router';

const LanguageSwitcher: React.FC = () => {
  const router = useRouter();

  const switchLanguage = (lang: string) => {
    const { pathname, query, asPath } = router;
    router.push({ pathname, query }, asPath, { locale: lang });
  };

  return (
    <div>
      <button onClick={() => switchLanguage('en')} className="text-white bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded">English</button>
      <button onClick={() => switchLanguage('ja')} className="text-white bg-blue-500 hover:bg-blue-600 px-4 py-2 rounded ml-2">日本語</button>
    </div>
  );
};

export default LanguageSwitcher;
