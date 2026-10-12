export type Lang = 'zh' | 'en';
export const defaultLang: Lang = 'zh';

export const ui = {
	zh: {
		'brand.main': '臺灣青少年科學發展協會',
		'brand.sub': 'Taiwan Young Science Development Association',
		'logo.alt': '臺灣青少年科學發展協會 logo',
		'nav.about': '關於我們',
		'nav.members': '協會成員',
		'nav.activities': '協會活動',
		'nav.charter': '組織章程',
		'menu.open': '開啟選單',
		'lang.switch': 'EN',
		'lang.switchLabel': 'Switch to English',
		'footer.copyright': '© 2026 臺灣青少年科學發展協會'
	},
	en: {
		'brand.main': 'Taiwan Young Science Development Association',
		'brand.sub': '臺灣青少年科學發展協會',
		'logo.alt': 'Taiwan Young Science Development Association logo',
		'nav.about': 'About Us',
		'nav.members': 'Members',
		'nav.activities': 'Activities',
		'nav.charter': 'Charter',
		'menu.open': 'Open menu',
		'lang.switch': '中文',
		'lang.switchLabel': '切換為中文',
		'footer.copyright': '© 2026 Taiwan Young Science Development Association'
	}
} as const;

export type UIKey = keyof typeof ui.zh;

export function useTranslations(lang: Lang) {
	return (key: UIKey): string => ui[lang][key] ?? ui[defaultLang][key];
}

export function getLangFromUrl(url: URL): Lang {
	const [, first] = url.pathname.split('/');
	return first === 'en' ? 'en' : 'zh';
}

/** 去掉 /en 前綴與結尾斜線，回傳中文版路徑，例如 /en/about/ → /about */
export function stripLang(pathname: string): string {
	let p = pathname.replace(/^\/en(?=\/|$)/, '');
	if (p === '') p = '/';
	if (p.length > 1 && p.endsWith('/')) p = p.slice(0, -1);
	return p;
}

/** 已經有英文版的頁面（以中文版路徑表示）。每完成一頁就加進來。 */
export const translatedPaths = new Set<string>(['/', '/about', '/members', '/charter', '/activities', '/activities/assembly', '/forum', '/forum/2026', '/forum/2026/schedule', '/forum/2026/speakers', '/forum/2026/register', '/forum/2026/register/form', '/forum/2026/invite']);

/** 依語言產生連結；英文版尚未完成的頁面會自動指向中文版。支援 #錨點。 */
export function localizePath(path: string, lang: Lang): string {
	const [base, hash] = path.split('#');
	const clean = stripLang(base);
	const suffix = hash ? `#${hash}` : '';
	if (lang === 'en' && translatedPaths.has(clean)) {
		return (clean === '/' ? '/en/' : `/en${clean}`) + suffix;
	}
	return clean + suffix;
}