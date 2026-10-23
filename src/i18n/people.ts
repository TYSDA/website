import type { Lang } from './ui';

export type PersonKey =
	| 'xie' | 'yuchih' | 'wang'
	| 'xuShizhan' | 'xuHezhen' | 'zhang'
	| 'cai' | 'gong' | 'huoqin' | 'wanglong' | 'ji' | 'li'
	| 'zheng' | 'shi' | 'xuWeiting'
	| 'gu' | 'guan' | 'e';

type Person = { zh: string; en: string; titleZh: string; titleEn: string };

// en 欄位填英文姓名（例如 'Chih-Liang Hsieh'）。留空時英文版會先顯示中文姓名與稱謂。
export const people: Record<PersonKey, Person> = {
	xie:       { zh: '謝至亮', en: 'Chih-Liang Hsieh', titleZh: '博士', titleEn: 'Dr.' },
	yuchih:    { zh: '尉遲和妘', en: 'Ho-Yun YuChih', titleZh: '', titleEn: '' },
	wang:      { zh: '王翊語', en: 'Yi-Yu Wang', titleZh: '', titleEn: '' },
	xuShizhan: { zh: '徐士展', en: 'Shih-Chan Hsu', titleZh: '', titleEn: '' },
	xuHezhen:  { zh: '許禾臻', en: 'Ho-Chen Hsu', titleZh: '', titleEn: '' },
	zhang:     { zh: '張雨恩', en: 'Yu-En Chang', titleZh: '', titleEn: '' },
	cai:       { zh: '蔡任圃', en: 'Jen-Pu Tsai', titleZh: '老師', titleEn: '' },
	gong:      { zh: '龔雍任', en: 'Yung-Jen Kung', titleZh: '老師', titleEn: '' },
	huoqin:    { zh: '劉火欽', en: 'Huo-Chin Liu', titleZh: '館長', titleEn: 'Director' },
	wanglong:  { zh: '李旺龍', en: 'Wang-Lung Lee', titleZh: '教授', titleEn: 'Prof.' },
	ji:        { zh: '紀凱容', en: 'Kai-Jung Chi', titleZh: '老師', titleEn: 'Prof.' },
	li:        { zh: '李後鋒', en: 'Hou-Feng Lee', titleZh: '老師', titleEn: 'Prof.' },
	zheng:     { zh: '鄭夢慈', en: 'Meng-Tzu Cheng', titleZh: '教授', titleEn: 'Prof.' },
	shi:       { zh: '施鈞瀚', en: 'Chun-Han Shih', titleZh: '博士', titleEn: 'Dr.' },
	xuWeiting: { zh: '徐偉婷', en: 'Wei-Ting Hsu', titleZh: '博士', titleEn: 'Dr.' },
	gu:        { zh: '顧廣毅', en: 'Kuang-Yi Ku', titleZh: '老師', titleEn: 'Asst. Prof.' },
	guan:      { zh: '關貫之', en: 'Kuan-Chih Kuan', titleZh: '老師', titleEn: '' },
	e:         { zh: '鄂禹臻', en: 'Yu-Chen E', titleZh: '老師', titleEn: '' }
};

export function personName(key: PersonKey, lang: Lang): string {
	const p = people[key];
	if (lang === 'en' && p.en) {
		return p.titleEn ? `${p.titleEn} ${p.en}` : p.en;
	}
	return `${p.zh}${p.titleZh}`;
}

/** 論壇講者英文名（以中文名為鍵）。講者頁與報名表單共用；name 留空時英文頁退回顯示中文。 */
export const speakerEn: Record<string, { name: string; title: string }> = {
	'謝至亮': { name: 'Chih-Liang Hsieh', title: 'Dr.' },
	'尉遲和妘': { name: 'Ho-Yun YuChih', title: '' },
	'王翊語': { name: 'Yi-Yu Wang', title: '' },
	'徐士展': { name: 'Shih-Chan Hsu', title: '' },
	'許禾臻': { name: 'Ho-Chen Hsu', title: '' },
	'張雨恩': { name: 'Yu-En Chang', title: '' },
	'蔡任圃': { name: 'Jen-Pu Tsai', title: '' },
	'龔雍任': { name: 'Yung-Jen Kung', title: '' },
	'紀凱容': { name: 'Kai-Jung Chi', title: 'Prof.' },
	'李後鋒': { name: 'Hou-Feng Lee', title: 'Prof.' },
	'鄭夢慈': { name: 'Meng-Tzu Cheng', title: 'Prof.' },
	'施鈞瀚': { name: 'Chun-Han Shih', title: 'Dr.' },
	'徐偉婷': { name: 'Wei-Ting Hsu', title: 'Dr.' },
	'顧廣毅': { name: 'Kuang-Yi Ku', title: 'Asst. Prof.' },
	'關貫之': { name: 'Kuan-Chih Kuan', title: '' },
	'鄂禹臻': { name: 'Yu-Chen E', title: '' }
};

export function speakerEnName(zh: string): string {
	return speakerEn[zh]?.name ?? '';
}


/** 非講者的理監事與秘書英文名（以中文名為鍵）；留空時英文頁退回顯示中文。 */
export const memberEn: Record<string, string> = {
	'邱俊禕': 'Chun-Wei Chiu',
	'莊宇權': 'Yu-Chuan Chuang',
	'胡芳碩': 'Fang-Shuo Hu',
	'王浩平': 'Hao-Ping Wang',
	'廖士宏': 'Shih-Hung Liao',
	'柳鈞元': 'Chun-Yuan Liu',
	'邱奕寧': 'Yi-Ning Chiu'
};

/** 先查講者表，再查成員表；都沒有就回傳空字串。 */
export function anyEnName(zh: string): string {
	return speakerEn[zh]?.name || memberEn[zh] || '';
}
