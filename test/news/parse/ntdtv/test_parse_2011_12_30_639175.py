import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ntdtv


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='新唐人')
    url = r'https://www.ntdtv.com/b5/2011/12/30/a639175.html'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.ntdtv.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            金正日的葬禮受到全世界的矚目。不過,看了朝鮮中央電視臺全程直播的葬禮過程,對朝鮮人
            在現場嚎啕大哭,頓足捶胸,痛心程度真如失去至親的情景,讓西方媒體頗為訝異,認為朝鮮人
            是否瘋了,似乎在舉行一場痛哭比賽。 自從金正日去世後,整個朝鮮正處於官方規定的
            哀悼期,29日上午,朝鮮十萬人參加了在平壤參加了金正日追悼大會。朝鮮委員長金永南
            致悼詞說,整個人類與我們共同處在這種悲痛當中,這足可以證明我們的領袖有多麽偉大;
            並強調朝鮮會化悲痛為力量、堅決擁護金正恩的思想。追悼大會在接近中午結束,現場鳴炮
            21響,人民默哀3分鐘。 29日金正日追悼大會,正午12點,所有的火車、輪船和汽車,同聲
            鳴笛、為金正日默哀3分鐘,12天國殤期的最後一天,數萬民眾湧進平壤市中心的一個廣場
            參加為金正日舉辦的全國追悼會。朝鮮國家電視臺顯示金日成廣場上擠滿了無數士兵,金正恩
            低頭致哀。 當天,朝鮮的朝鮮中央電視臺全程直播了載有金正日靈柩的靈車車隊從平壤
            錦繡山紀念宮出發,經過金日成廣場和平壤市內主要街道繞行一圈的場面。靈車經過的道路
            兩旁聚集了數十萬平壤市民,臉和手已被凍得發紅。但幾乎看不到帶傘或戴帽子的人,他們
            的頭發和衣服也都被雪水浸濕。 美國時事週刊《時代》就28日金正日送別儀式說,今日,
            朝鮮媒體向全球播放的金正日遺體告別儀式場面一定是我們所看到的最為超現實的國家劇場
            一景......哀悼的大部分民眾沒有抑制悲痛嚎啕大哭,所有的吶喊聲、呻吟聲、痛哭昏厥的
            動作通過國家電視臺的鏡頭多角度準確地抓拍。」。 《時代》還通過一篇標題為《偉大
            的朝鮮痛哭比賽》的文章寫道:「在金正日遺體告別儀式上,朝鮮人民一定會使出渾身力氣
            痛哭,而全世界的人看到此景會想『難道這些人都瘋了嗎?』。」 美聯社報道說:「載有
            金正日靈柩的靈車駛過白雪覆蓋的平壤市區時,數十萬平壤市民聚集在道路兩旁拍著胸脯
            痛哭。 法新社則嘲諷道:「在哀樂聲中,熒屏上播放了在這個核武裝的國家裏,長達17年
            掌握絕對權力、讓數萬名民眾在饑餓中死去的『親愛的領導人』所走過的道路。」 日本
            產經新聞12月28日報導,朝鮮當局強制朝鮮居民哀悼金正日,工廠、企業每天規定了固定的
            哀悼時間,百姓被強制要求1天必須哭兩次,1次1小時。有朝鮮百姓說:「已經哭的沒有眼淚
            了,但是不哭的話就會被強制帶走,我們只好裝著哭,大聲的哭。」 報導還說,在朝鮮哀悼
            場所,都有朝鮮公安進行監視,不哭的人就會被帶走,在朝鮮坐火車,必須先哭才能上火車,
            不哭就會被強制趕下去。 大陸網絡對金正日葬禮也熱議不絕。 有網友說,去朝鮮出差,
            回國前剛好趕上金正日的葬禮。他們在火車上被要求痛哭,哭不出來不允許回國。 網友麼麼
            說:外國媒體說朝鮮人是演戲,其實不是。他們都是從小被訓練出來的,知道什麼時候該哭,
            什麼時候該笑,什麼時候該義憤填膺,已經成為本能了。這種本能如果培養得不好,很可能
            被槍斃。 網友快樂的老貓說:蒼天有眼讓我們笑看這個世界上一個個狗雜碎的獨裁們下地獄,
            是人都快樂的無比,誰悲痛了呢? 網友連鵬:金正日追悼大會,朝鮮人民會議委員長金永南
            發表悼詞,稱「整個人類與我們共同處在這種悲痛當中。」——金正日真是魅力十足的領袖,
            所以,朝鮮人民寧願忍饑挨餓,甚至餓死,也要把他們一家養得胖嘟嘟的。 毛澤東死,中國也有
            痛哭比賽 這些天播出朝鮮民眾對於金正日去世和葬禮的強烈反應,中外媒體都忍不住和當年
            毛澤東死亡的時候中國人的反應相比較。網友比較,那時的中國人民哭的與朝鮮相比,有過之
            而無不及。 作家黃文權在他所著的《紅小兵:一個家庭的回憶錄》中這樣描述:一宣佈完
            宣佈消息,老師就開始嚎啕大哭,我們班裏的許多女孩子也跟著哭了起來。我們這幫男孩
            不知道怎麼辦,不過擔心被人家說成對毛主席不那麼熱愛,我們想辦法擠出眼淚來。這樣做
            真的不容易,因為毛雖然偉大,我們卻的確對他不瞭解。 他說,他想起了家裏生病的奶奶。
            連毛主席都會死,她也會死的。然後很快留下了真的眼淚。很快,就哭得昏了過去,引來了
            學校的護士。 他回憶:“學校給我們發了黑色的孝帶和白色的小花。沒有人敢說笑話,沒有人
            敢笑。無論走到哪里,都能看到黑邊的毛的畫像,四周擺放著花圈。單位組織成千上萬的民眾
            到西安中心的人民廣場(其實應該是新城廣場)。他們先是靜靜地跪在毛主席的畫像前,後來
            有人哭了起來。很快,整個人群哭成一片,人們捶胸頓足,嚎啕大哭,活像一場痛哭
            比賽。 黃文權在文章中寫道:在某種程度上,他們是在比誰更忠於毛主席。城裏所有的娛樂
            活動都被禁止。喇叭裏終日播送一樣的哀樂。我們學校裏,每班選4名同學輪流在毛主席像
            壇前站崗,每班4小時。 他回憶,北京舉行毛主席追悼大會的那天下著大雨。“天神都為
            毛主席落淚,”老師一本正經地說。“過去皇帝去世時總會這樣。”在聽悼念大會的實況轉播
            時,他的一個同學放了一個屁,大家都咯咯笑了起來。那位學生的母親是一所醫院的
            護士長,後來提交了醫療證明,證明消化不良,他才沒有被開除。 他認為,對毛主席逝世表現出
            劇烈的悲痛其實是一種政治需要。 黃文權說,看到在金正日的葬禮上,跟他的父母和老師
            一樣的人——有些人為失去神一般的人真的感到悲傷,另一些人出於恐懼而置身於喪禮期間
            的表演。他們知道,不這樣做,他們或者他們的家庭就會受到指責。 他表示,35年過去了,
            現在看到暴政依然在朝鮮發出迴響,真令人感到噁心。
            '''
        ),
    )
    assert parsed_news.category == '國際,時政'
    assert parsed_news.company_id == company_id
    assert parsed_news.datetime == 1325174400
    assert parsed_news.reporter is None
    assert parsed_news.title == '西媒看金正日葬禮:朝鮮人瘋了?在痛哭比賽'
    assert parsed_news.url_pattern == '2011-12-30-639175'
