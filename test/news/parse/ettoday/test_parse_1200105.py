import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.ettoday


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='東森')
    url = r'https://star.ettoday.net/news/1200105'
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

    parsed_news = news.parse.ettoday.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            約莫一個月前,最高法院針對一起賭博案件進行的調查程序,聽取了專家學者的意見。案件
            並不複雜,但是因為涉及到了現代通訊技術及法制上不盡完備的地方,所以引起了許多的注
            意。最高法院在這一個案件中,未囿於既有法規的文字,著眼於通訊的樣態、往來模式,以及
            人們隱私保護的需要,判定偵查機關向電信業者等第三人調取用戶的電子郵件時,必須遵循
            令狀原則,事先取得法院授權。這個判決的結論,賦予了人民在科技日新月異的時代,更為週
            延的隱私保障,也兼顧了犯罪偵查的實際需要,值得肯定(最高法院106年度台非字第259號判
            決)。 這一個案件的事實大致是:被告使用中華電信所提供的Hibox服務經營六合彩賭博,
            Hibox會將賭客的傳真的簽單以電子郵件的方式寄送到被告的電子郵件信箱中。檢察官向法院
            聲請通聯記錄調取票獲准後,從中華電信取得了被告已收受的電子郵件。這一個案件的爭點
            因而是,偵查機關應依照什麼樣的程序,才能取得被告已經讀取過的電子郵件? 在進到最高
            法院的說理及分析前,必須要先說明的是刑事訴訟法(以下簡稱「刑訴法」)及通訊保障及監
            察法(以下簡稱「通保法」)的幾個重要規定。 第一,是扣押。刑訴法第133條之1規定,原則
            上,要以不經搜索而發動的扣押取得純為證據之物時,檢察官得依職權核發扣押命令,但若是
            要取得得沒收之物,就必須要經過法院授權。 第二,通聯記錄的調取。依通保法,為偵查重
            大犯罪,檢察官得向法院聲請核發調取票,向電信業者調取特定人的通話往來紀錄(通保法第
            11條之1)。要注意的是,這一類的紀錄只涵蓋了電話號碼、通話時間、長度等不涉及通訊內
            容的事項。 第三,通訊監察。依通保法,為偵查重大犯罪,在經法院核發通訊監察書後,檢警
            官員得監察犯罪嫌疑人的通訊內容(通保法第5條)。 在本件判決,最高法院首先指出,通訊
            發出,為收受者所接收後,就已經不再是憲法第16條祕密通訊自由所要保護的對象,沒有通保
            法中通訊監察書的適用。判決進一步說明,之所以在一般隱私之外,特別保護「通訊隱私」,
            是因為通訊涉及到兩個以上的參與人,以祕密的方式或狀態,透過介質或媒體,傳遞或是交換
            不欲為他人所知的訊息。訊息在傳遞的過程中,不受通訊參與者所控制,更容易受到第三人
            或國家的侵擾。這是一種特別情形。也因此,一旦訊息為收受者所接收,訊息就不再屬於通
            訊隱私,但仍受有一般隱私權的保護。是故,檢警官員要取得通訊參與者已經接收的訊息,不
            需要向法院聲請「通訊監察書」。這部份與美國、德國及日本的法制及實務運作完全一致
            。再者,因為收受者接收,已經儲存下來的訊息內容不只是通聯記錄,所以也不能以「調取票
            」為之。 接下來的問題是,偵查官員應該要以什麼方式取得通訊參與者已經接收的訊息?是
            檢察官的扣押命令?還是必須事先取得法院所核發的令狀(扣押裁定)?就此,最高法院作成了
            極為重要且令人振奮的宣示:已經接收的通訊雖然不再為通訊隱私所涵蓋,但是仍受有一般
            隱私的保護,所以有令狀原則的適用—應事先取得法院裁定。最高法院更進一步地說明道,在
            現今資訊社會,人們大量使用各樣的通訊服務,第三方因而持有大量極為個人且私密的訊息
            內容,如果不採令狀原則,檢警機關將可以逕自調閱,對人民的隱私將造成莫大的戕害。再者
            ,若容許檢察官得逕自以扣押命令為之,在向外國通訊服務或軟體公司(如Google、Facebook
            或Line等)調取訊息內容時,它們勢必要考量檢察官的扣押命令是否合於其本國法律,如該國
            就這一類訊息的調取採令狀原則,就會拒絕檢察官等偵查人員的要求,如此一來反而有害於
            犯罪的有效偵查。因此,雖然儲存於電信公司或通訊服務業者的訊息純為證據,但最高法院
            以隱私保護及犯罪偵查的有效進行為理由,判定偵查官員還是必須「事先獲有法院授權」,
            才能夠調取。 最高法院針對此一爭議的說理,無論是在政策上的分析或是價值決定,都兼顧
            了人民隱私保護的需要及犯罪的有效偵查,值得肯定讚賞。深入探究後就可以知道,若是選
            擇了以「調取票」或「通訊監察書」方得為之,會有重罪原則(輕罪案件不能調取)的要求,
            在非常大範圍的案件偵查中,將無法調取特定人已經接收的訊息,會大幅降低犯罪偵查的效
            率。相反地,若容許檢察官以「扣押命令」為之,人民的隱私將完全暴露在偵查權限之下,沒
            有第三者的控制,極為不妥。最高法院最後的判定(應事前取得法院之扣押裁定),平衡了兩
            者的需要,可謂妥適合理。 值得附帶一提的是,類似的問題不只發生在我國,也深深困擾著
            美國的學界及實務。美國聯邦第六巡迴法院在United States v. Warshak案曾判定,人們對
            於儲存於第三方的電子郵件享有聯邦憲法上的隱私權,不過,聯邦最高法院尚未為就此表示
            意見。聯邦國會也因而開始討論電子郵件的隱私,並且擬定各樣的法案。對比之下,前述我
            國最高法院的判決毫不遜色,甚至是更為合宜。不過,必須要承認的是,作為司法機關,這幾
            乎已經是最高法院的極限。嚴格來說,刑訴法的扣押裁定並無法完全滿足訊息調取的需要。
            接下來,還有賴立法者就此形成更為完整的規範。 最後,從文字上來說,扣押裁定的對象是
            「物」(刑訴法第133條之1參照),是否可以適用「訊息」?就此,可以說明的是,訊息本身是
            電磁型態的紀錄或資訊,本身不可能單獨被持有或扣押。訊息必須要附著於特定物品上,如
            紙張、隨身碟、光碟或硬碟上,才可能被保存或使用。也因此,扣押裁定當然不是(也不可能
            是)針對訊息本身,而是就附著或儲存有訊息的物品。不過,不能否認的是,這樣的解釋並不
            能完全解決所有的問題,刑訴法及通保法在立法及歷次的修正中,顯然也沒有意識條文文字
            中的問題。也因此,釜底抽薪之計,還是必須即早就此修正相關法律,方得使執法機關有所依
            循,人民也才能享有應有的隱私權益。 李榮耕,國立台北大學法律學系教授。
            '''
        ),
    )
    assert parsed_news.category == '雲論'
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1530069600
    assert parsed_news.reporter is None
    assert parsed_news.title == '為最高法院保障人民隱私權的判決按讚!'
    assert parsed_news.url_pattern == '1200105'