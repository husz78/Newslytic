from flask import Blueprint, render_template, request
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    sources = ["cnn.com", "bbc.co.uk", "channel4.com", "vox.com", "traxnews.org", "247newsaroundtheworld.com",
    "blogspot.com", "reviewminute.com", "theasialive.com", "breakingasia.com", "globalissues.org", "gudstory.com",
    "theunionjournal.com", "zimonews.com", "egyptian-gazette.com", "cbslocal.com", "cyberethiopia.com", "karennews.org",
    "afgha.com", "informalnewz.com", "maoritelevision.com", "focusguinee.info", "revuemag.com", "go.com", "biv.com",
    "timesofnews.com", "chinafilminsider.com", "cocorioko.net", "connachttribune.ie", "dailyfinland.fi",
    "eldjazaironline.dz", "chosun.com", "elpais.com", "expresochiapas.com", "lastampa.it", "dahaboo.com",
    "beijingbulletin.com", "dublinnews.com", "breitbart.com", "express.co.uk", "euronews.com", "financialpost.com",
    "independentaustralia.net", "ndtv.com", "ruralnewsgroup.co.nz", "scroll.in", "socialsamosa.com", "time.com",
    "foxnews.com", "news24.com", "sky.com", "sydneysun.com", "thejapannews.net", "t-online.de", "washingtonpost.com",
    "gp.se", "finlandtoday.fi", "greenlandtoday.com", "grupometropoli.net", "ifpnews.com", "imparcialoaxaca.mx",
    "indaily.com.au", "lesoleil.sn", "levenementprecis.com", "montserrat-newsletter.com", "mvariety.com", "naimexico.com",
    "zeit.de", "newuthayan.com", "rivira.lk", "cbc.ca", "lankapuvath.lk", "standardtimespress.org", "tass.com",
    "theconversation.com", "theforeigner.no", "theresident.eu", "timesofsandiego.com", "trinidadexpress.com", "tvm.mr",
    "9news.com.au", "acn.cu", "adaderana.lk", "addisadmassnews.com", "aljazeera.com", "aopnews.com", "asiatoday.com",
    "bahrainmirror.com", "barrierestarjournal.com", "bbs.bt", "burnslakelakesdistrictnews.com", "businessnews.com.au",
    "cambridge-news.co.uk", "campbellrivermirror.com", "channelnewsasia.com", "ctvnews.ca",
    "dailymail.co.uk?ns_mchannel=rss&ns_campaign=1490&ito=1490", "daily-mail.co.zm", "diariosigloxxi.com",
    "digitalmarket.asia", "ekonomist.rs", "elvocero.com", "financialexpress.com", "guampdn.com", "hitsfm.com.np",
    "huffingtonpost.co.uk", "independent.co.uk", "industryandbusiness.ie", "inp.net.pk", "kelownacapnews.com",
    "kimberleybulletin.com", "koreaherald.com", "langleyadvancetimes.com", "lesahel.org", "madonline.com", "follow.it",
    "metrotimes.com", "mirror.co.uk", "newsonjapan.com", "newsweek.com", "npr.org", "peacearchnews.com", "politico.com",
    "riverfronttimes.com", "sana.sy", "seychellesnewsagency.com", "slguardian.org", "smh.com.au", "standard.co.uk",
    "sunnysouthnews.com", "tamtaminfo.com", "techcentral.ie", "thestar.com", "theweek.com", "times.co.sz", "times.co.zm",
    "tribune242.com", "tv6tnt.com", "tvr.ro", "uzreport.com", "vernonmorningstar.com", "virginislandsdailynews.com", "voxy.co.nz",
    "washingtontimes.com", "youngchinabiz.com", "cbn.com", "or.jp", "8columnas.com.mx", "abc13.com", "abc7news.com",
    "addisfortune.news", "addisstandard.com", "adevarul.ro", "australianjewishnews.com", "press.ma", "albiladdaily.com",
    "alicespringsnews.com.au", "allafrica.com", "amap.ml", "amnestynepal.org", "antigua-barbuda.com", "antiguaobserver.com",
    "sverigesradio.se", "articleify.com", "nikkei.com", "asianmilitaryreview.com", "astanatimes.com", "atop.tg", "aujourdhui.ma",
    "barbadostoday.bb", "benininfo.com", "bernews.com", "burkina24.com", "business-review.eu", "calgaryherald.com",
    "calgarysun.com", "canal4rd.com", "carnewschina.com", "chinaglobalsouth.com", "china-underground.com", "cphpost.dk",
    "cpj.org", "crowdwisdom.live", "libsyn.com", "dailypost.ng", "dailytimes.com.pk", "kyiv.ua", "dayakdaily.com",
    "diario.mx", "elmundo.es", "e27.co", "economist.com.na", "edmontonjournal.com", "edmontonsun.com", "elbcradio.com",
    "eldeforma.com", "eleftherostypos.gr", "elperiodico.com.gt", "desk-russie.eu", "mehrnews.com", "mercopress.com", 
    "kyodonews.net", "radio.cz", "englishrussia.com", "ethsat.com", "podbean.com", "chandigarhcitynews.com", "nezavisne.com",
    "sdpnoticias.com", "thelocal.com", "fraternitenews.info", "gcn.ie", "globalnews.ca", "globalpressjournal.com",
    "gothamist.com", "groupelavenir.org", "guineenews.org", "guyanachronicle.com", "haitiantimes.com",
    "homesandinteriorsscotland.com", "hongkongfp.com", "hrmasia.com", "ialtchad.com", "imemc.org", "wordpress.com", 
    "philenews.com", "independent.ng", "indianexpress.com", "indiannewsqld.com.au", "indiaobservers.com", "internetprotocol.co",
    "itb.com", "ittn.ie", "japaninsides.com", "japantoday.com", "jurnalul.ro", "kalkinemedia.com", "kayhan.ir", "khabar.kz",
    "khmertv.com", "kosovapress.com", "krooknews.com", "kurier.at", "kwttoday.com", "lanka24news.com", "leaderpost.com",
    "leadership.ng", "lenews.ch", "andavamamba.com", "live24.lk", "lnr.org.la", "londonjournal.co.uk", "lovefm.com", "lzinios.lt",
    "makfax.com.mk", "maldivesindependent.com", "mb.com.ph", "mediaindonesia.com", "mediapermata.com.bn", "meduza.io",
    "mexiconewsdaily.com", "mmbiztoday.com", "monacolife.net", "mondediplo.com", "montrealgazette.com", "munichnow.com",
    "myawady.net.mm", "nation.com.pk", "nation.lk", "nationalpost.com", "news.ai", "google.com", "livedoor.com", "ltn.com.tw",
    "stv.tv", "news4masses.com", "newsblare.com", "newsday.co.tt", "newsin.asia", "newsnblogs.com", "newsnet.scot", "nypost.com",
    "oakvillenews.org", "obn.ba", "observer.com", "globo.com", "ortb.bj", "ottawacitizen.com", "ottawasun.com", "ozzienews.com",
    "pbsguam.org", "peru.com", "pina.com.fj", "politiken.dk", "pridnestrovie-daily.net", "freepressjournal.in", "thequint.com",
    "punchng.com", "quintdaily.com", "rabble.ca", "rightwirereport.com", "sueddeutsche.de", "idnes.cz", "shabait.com", "sic.pt",
    "sloveniatimes.com", "sltn.co.uk", "sluggerotoole.com", "smallwarsjournal.com", "soranews24.com", "southeastasiaglobe.com",
    "sme.sk", "splash247.com", "standforfreedom.ca", "starofmysore.com", "startupreporter.in", "abc.es", "stcroixsource.com", 
    "sudantribune.com", "thechinaproject.com", "tribunnews.com", "surgezirc.co.uk", "talkingupscotlandtwo.com", "taz.de",
    "technode.com", "thebridge.jp", "thediplomat.com", "thefrontierpost.com", "thegambiaradio.com", "theintercept.com",
    "theiranproject.com", "thenassauguardian.com", "thenewdawnliberia.com", "thenewshimachal.com", "theorkneynews.scot",
    "theparisnews.com", "theprovince.com", "thestandard.org.nz", "thestarphoenix.com", "tibettimes.net", "ticotimes.net",
    "tiempo.hn", "times.mw", "indiatimes.com", "togopresse.tg", "citynews.ca", "torontosun.com", "uacrisis.org", "urbana.com.py",
    "uscnpm.org", "vancouversun.com", "vanguardia.com.mx", "vecer.mk", "villagemagazine.ie", "vladnews.ru", "vob929.com",
    "voxeurop.eu", "wan-ifra.org", "warontherocks.com", "warritatafo.com", "whdh.com", "gazeta.pl", "windsorstar.com", "wsvn.com",
    "24chasa.bg", "24-horas.mx", "24sata.hr", "abbynews.com", "abc.net.au", "acap.cf", "adworld.ie", "aftenposten.no",
    "agassizharrisonobserver.com", "agriland.ie", "aib.media", "alalam.ma", "albayan.ae", "albayan.aehttps", "aletihad.ae",
    "altoadige.it", "amnesty.org", "aninews.in", "anphoblacht.com", "apnlive.com", "artscouncil.ie", "asianexpress.co.uk",
    "asiasentinel.com", "autonews.com", "northernirelandworld.com", "belfastlive.co.uk", "bhaskarlive.in", "bhutannewsservice.org",
    "bordertelegraph.com", "boston.com", "bostonherald.com", "breakingnewstoday.co.uk", "brookings.edu", "buchanobserver.co.uk",
    "budapesttimes.hu", "business-standard.com", "campaignasia.com", "canberratimes.com.au", "capital.bg", "capitalqueretaro.com.mx",
    "osvnews.com", "cbsnews.com", "ceskenoviny.cz", "challenge.ma", "chanarcillo.cl", "chicagotribune.com", "chinaentertainmentnews.com",
    "chosonsinbo.com", "churchofscotland.org.uk", "thecjn.ca", "cnbc.com", "computerworld.com", "costa-news.com", "cricketireland.ie",
    "crtv.cm", "ctitv.com.tw", "cubanet.org", "dailyexcelsior.com", "dailyherald.com", "dailyheraldtribune.com", "dailynews.co.th",
    "dailypolitics.com", "dailypost.vu", "dailyrecord.co.uk", "danas.rs", "dayniiile.com", "dbsuriname.com", "deadlinenews.co.uk",
    "debate.com.mx", "deccanchronicle.com", "delfi.lv", "derryjournal.com", "deutschland.de", "diariocolatino.com", "gouv.fr?xtor=RSS-1",
    "dnaindia.com", "dnevnik.bg", "dnevnik.si", "donegaldaily.com", "dv.is", "eastasiaforum.org", "easternherald.com", "scotsman.com",
    "efe.com", "egyptindependent.com", "elcorreo.com", "eldiario.com.co", "eldiario.net", "elfinanciero.com.mx", "elnorte.com", 
    "elsiglodetorreon.com.mx", "eluniversal.com.mx", "el-universal.com", "emirates247.com", "ena.et", "esmitv.com", "europeantimes.news",
    "expatica.com", "fanabc.com", "faz.net", "financeasia.com", "firstpostofindia.com", "fleet.ie", "france24.com", "francetvinfo.fr",
    "ft.com", "glasgowlive.co.uk", "glasgowtimes.co.uk", "globes.co.il", "gnlm.com.mm", "goulburnpost.com.au", "atom.xml", "gov.br",
    "grampianonline.co.uk", "grenadabroadcast.com", "grimsbytelegraph.co.uk", "gs.by", "handelsblatt.com", "headlinesoftoday.com",
    "helsinkitimes.fi", "heraldscotland.com", "hoy.es", "huffpost.com", "iaasiaonline.com", "ibtimes.com.au", "ilmattino.it", 
    "ilmessaggero.it", "ilsole24ore.com", "iltalehti.fi", "iltempo.it", "independent.ie", "indiatoday.in", "inform.kz",
    "informador.mx", "insider.co.uk", "interfax.ru", "inverness-courier.co.uk", "iraqhurr.org", "irish-boxing.com",
    "irishbuildingmagazine.ie", "irishcentral.com", "irishmirror.ie", "irishtimes.com", "islandsun.com", "itnnews.lk",
    "ittefaq.com.bd", "iwacu-burundi.org", "iwnsvg.com", "japantimes.co.jp", "jasarat.com", "jornada.com.mx", 
    "journaldutogo.com", "jurnal.md", "kaieteurnewsonline.com", "kanivatonga.co.nz", "kbc.co.ke", "kentnews.online",
    "kilkennypeople.ie", "kiwikidsnews.co.nz", "kuwaittimes.com", "lacittadisalerno.it", "la-croix.com", "lahora.com.ec",
    "lanacion.cl", "lanation.dj", "lankabusinessonline.com", "laprensagrafica.com", "latimes.com", "latribune.fr", "laweekly.com",
    "lemonde.fr", "liberoquotidiano.it", "libertas.sm", "libertatea.ro", "limerickleader.ie", "lusakavoice.com", "macleans.ca",
    "madagascar-tribune.com", "majorcadailybulletin.com", "mbl.is", "meanwhileinireland.com", "mediapart.fr", "mediareform.org.uk",
    "mercurynews.com", "middleeastmonitor.com", "minnpost.com", "monde-diplomatique.fr", "mwnation.com", "naftemporiki.gr",
    "naharnet.com", "nationalobserver.com", "navhindtimes.in", "nbcchicago.com", "nbcmiami.com", "nbcwashington.com", "necn.com",
    "nepalitimes.com", "neweurope.eu", "news.lk", "newsagencyblog.com.au", "newsrust.com", "notiziegeopolitiche.net",
    "novamakedonija.com.mk", "novilist.hr", "novinite.com", "ntv.ru", "nv-online.info", "nyasatimes.com", "nytimes.com",
    "oneindia.com", "onlanka.com", "orissapost.com", "timeschronicle.ca", "ouestribune-dz.com", "owensoundsuntimes.com",
    "ozodi.org", "pakistantoday.com.pk", "peachlandview.com", "pembrokeobserver.com", "perthnow.com.au", "phillyvoice.com",
    "phnompenhpost.com", "thepinknews.com", "politico.eu", "politics.co.uk", "popularmyanmar.com", "positive.news", 
    "powersportz.tv", "premiumtimesng.com", "prensa-latina.cu", "prensalibre.com", "pressandjournal.co.uk", "theworld.org",
    "publimetro.com.mx", "publishedreporter.com", "radiohc.cu", "radiondekeluka.org", "rand.org", "rappler.com", "rawstory.com",
    "razon.com.mx", "reforma.com", "repubblica.it", "retailnews.asia", "rfa.org", "rfi.fr", "rm.co.mz", "rsvplive.ie", "rtb.bf",
    "rtrs.tv", "rts.rs", "rttlep.tl", "saanichnews.com", "sabcnews.com", "saipantribune.com", "salon.com", "sbs.com.au", "scmp.com",
    "scoop.co.nz", "scottishfield.co.uk", "shetlandtimes.co.uk", "sibconline.com.sb", "sidwaya.info", "sinceindependence.com",
    "sn.at", "solomonstarnews.com", "euronews247.com", "spiegel.de", "sta.si", "stluciamirroronline.com", "capsula.sa", "straight.com",
    "stratfordbeaconherald.com", "sudquotidien.sn", "sundaypost.com", "svd.se", "tagesschau.de", "tahitinews.co", "techgenyz.com",
    "telegraaf.nl", "telegraph.co.uk", "teluguglobal.com", "tempo.com.ph", "tentaran.com", "the42.ie", "theage.com.au",
    "theargus.co.uk", "theboltonnews.co.uk", "thecourier.co.uk", "thedailymash.co.uk", "thedailyscrumnews.com", "theflorentine.net",
    "thefridaytimes.com", "the-gazette.co.uk", "theguardian.com", "thejc.com", "thejournal.ie", "theleader.info",
    "themontserratreporter.com", "thenationalherald.com", "thenews.mx", "thenorthernecho.co.uk", "thenorthlines.com",
    "theolivepress.es", "thepoke.com", "thescarboroughnews.co.uk", "theseasidegazette.com", "thestkittsnevisobserver.com",
    "thetimesofbengal.com", "theyucatantimes.com", "thisdaylive.com", "times.co.nz", "timpul.md", "topky.sk", "tvm.co.mz",
    "twincities.com", "utusan.com.my", "vaticannews.va", "vecernji.hr", "vg.no", "vicnews.com", "vijesti.me", "vikalpa.org",
    "virakesari.lk", "volksblatt.li", "watchdoguganda.com", "wort.lu", "woxx.lu", "wprost.pl", "yabiladi.com", "yahoo.com",
    "yorkpress.co.uk", "youtube.com", "ziaruldeiasi.ro", "zlv.lu", "euobserver.com", "znsbahamas.com", "welt.de", "focus.de",
    "bild.de", "wissenschaft.de", "spektrum.de", "forschung-und-wissen.de", "reddit.com", "kyivpost.com", "theepochtimes.com",
    "dailywire.com", "thedispatch.com", "reason.com", "reuters.com", "hurriyet.com.tr", "yenisafak.com", "internethaber.com",
    "rferl.org", "haaretz.com", "sport.ua", "isport.ua"]
    return render_template('base.html', sources = sources)

@main_bp.route('/api', methods=['POST'])
def api():
    # API URL and key
    api_url = 'https://api.worldnewsapi.com/search-news'
    api_key = '81ffe890f50d4d81a8981fd178df573a' # Later requires to be hidden and changed

    # These are the categories that the API supports
    categories = ["politics", "sports", "business", "technology", "entertainment", "health", "science",
                  "lifestyle", "travel", "culture", "education", "environment", "other"]
    selected_categories = ""
    
    selected_sources = request.form.getlist('sources')
    sources = ["cnn.com", "bbc.co.uk", "channel4.com", "vox.com", "traxnews.org", "247newsaroundtheworld.com",
    "blogspot.com", "reviewminute.com", "theasialive.com", "breakingasia.com", "globalissues.org", "gudstory.com",
    "theunionjournal.com", "zimonews.com", "egyptian-gazette.com", "cbslocal.com", "cyberethiopia.com", "karennews.org",
    "afgha.com", "informalnewz.com", "maoritelevision.com", "focusguinee.info", "revuemag.com", "go.com", "biv.com",
    "timesofnews.com", "chinafilminsider.com", "cocorioko.net", "connachttribune.ie", "dailyfinland.fi",
    "eldjazaironline.dz", "chosun.com", "elpais.com", "expresochiapas.com", "lastampa.it", "dahaboo.com",
    "beijingbulletin.com", "dublinnews.com", "breitbart.com", "express.co.uk", "euronews.com", "financialpost.com",
    "independentaustralia.net", "ndtv.com", "ruralnewsgroup.co.nz", "scroll.in", "socialsamosa.com", "time.com",
    "foxnews.com", "news24.com", "sky.com", "sydneysun.com", "thejapannews.net", "t-online.de", "washingtonpost.com",
    "gp.se", "finlandtoday.fi", "greenlandtoday.com", "grupometropoli.net", "ifpnews.com", "imparcialoaxaca.mx",
    "indaily.com.au", "lesoleil.sn", "levenementprecis.com", "montserrat-newsletter.com", "mvariety.com", "naimexico.com",
    "zeit.de", "newuthayan.com", "rivira.lk", "cbc.ca", "lankapuvath.lk", "standardtimespress.org", "tass.com",
    "theconversation.com", "theforeigner.no", "theresident.eu", "timesofsandiego.com", "trinidadexpress.com", "tvm.mr",
    "9news.com.au", "acn.cu", "adaderana.lk", "addisadmassnews.com", "aljazeera.com", "aopnews.com", "asiatoday.com",
    "bahrainmirror.com", "barrierestarjournal.com", "bbs.bt", "burnslakelakesdistrictnews.com", "businessnews.com.au",
    "cambridge-news.co.uk", "campbellrivermirror.com", "channelnewsasia.com", "ctvnews.ca",
    "dailymail.co.uk?ns_mchannel=rss&ns_campaign=1490&ito=1490", "daily-mail.co.zm", "diariosigloxxi.com",
    "digitalmarket.asia", "ekonomist.rs", "elvocero.com", "financialexpress.com", "guampdn.com", "hitsfm.com.np",
    "huffingtonpost.co.uk", "independent.co.uk", "industryandbusiness.ie", "inp.net.pk", "kelownacapnews.com",
    "kimberleybulletin.com", "koreaherald.com", "langleyadvancetimes.com", "lesahel.org", "madonline.com", "follow.it",
    "metrotimes.com", "mirror.co.uk", "newsonjapan.com", "newsweek.com", "npr.org", "peacearchnews.com", "politico.com",
    "riverfronttimes.com", "sana.sy", "seychellesnewsagency.com", "slguardian.org", "smh.com.au", "standard.co.uk",
    "sunnysouthnews.com", "tamtaminfo.com", "techcentral.ie", "thestar.com", "theweek.com", "times.co.sz", "times.co.zm",
    "tribune242.com", "tv6tnt.com", "tvr.ro", "uzreport.com", "vernonmorningstar.com", "virginislandsdailynews.com", "voxy.co.nz",
    "washingtontimes.com", "youngchinabiz.com", "cbn.com", "or.jp", "8columnas.com.mx", "abc13.com", "abc7news.com",
    "addisfortune.news", "addisstandard.com", "adevarul.ro", "australianjewishnews.com", "press.ma", "albiladdaily.com",
    "alicespringsnews.com.au", "allafrica.com", "amap.ml", "amnestynepal.org", "antigua-barbuda.com", "antiguaobserver.com",
    "sverigesradio.se", "articleify.com", "nikkei.com", "asianmilitaryreview.com", "astanatimes.com", "atop.tg", "aujourdhui.ma",
    "barbadostoday.bb", "benininfo.com", "bernews.com", "burkina24.com", "business-review.eu", "calgaryherald.com",
    "calgarysun.com", "canal4rd.com", "carnewschina.com", "chinaglobalsouth.com", "china-underground.com", "cphpost.dk",
    "cpj.org", "crowdwisdom.live", "libsyn.com", "dailypost.ng", "dailytimes.com.pk", "kyiv.ua", "dayakdaily.com",
    "diario.mx", "elmundo.es", "e27.co", "economist.com.na", "edmontonjournal.com", "edmontonsun.com", "elbcradio.com",
    "eldeforma.com", "eleftherostypos.gr", "elperiodico.com.gt", "desk-russie.eu", "mehrnews.com", "mercopress.com", 
    "kyodonews.net", "radio.cz", "englishrussia.com", "ethsat.com", "podbean.com", "chandigarhcitynews.com", "nezavisne.com",
    "sdpnoticias.com", "thelocal.com", "fraternitenews.info", "gcn.ie", "globalnews.ca", "globalpressjournal.com",
    "gothamist.com", "groupelavenir.org", "guineenews.org", "guyanachronicle.com", "haitiantimes.com",
    "homesandinteriorsscotland.com", "hongkongfp.com", "hrmasia.com", "ialtchad.com", "imemc.org", "wordpress.com", 
    "philenews.com", "independent.ng", "indianexpress.com", "indiannewsqld.com.au", "indiaobservers.com", "internetprotocol.co",
    "itb.com", "ittn.ie", "japaninsides.com", "japantoday.com", "jurnalul.ro", "kalkinemedia.com", "kayhan.ir", "khabar.kz",
    "khmertv.com", "kosovapress.com", "krooknews.com", "kurier.at", "kwttoday.com", "lanka24news.com", "leaderpost.com",
    "leadership.ng", "lenews.ch", "andavamamba.com", "live24.lk", "lnr.org.la", "londonjournal.co.uk", "lovefm.com", "lzinios.lt",
    "makfax.com.mk", "maldivesindependent.com", "mb.com.ph", "mediaindonesia.com", "mediapermata.com.bn", "meduza.io",
    "mexiconewsdaily.com", "mmbiztoday.com", "monacolife.net", "mondediplo.com", "montrealgazette.com", "munichnow.com",
    "myawady.net.mm", "nation.com.pk", "nation.lk", "nationalpost.com", "news.ai", "google.com", "livedoor.com", "ltn.com.tw",
    "stv.tv", "news4masses.com", "newsblare.com", "newsday.co.tt", "newsin.asia", "newsnblogs.com", "newsnet.scot", "nypost.com",
    "oakvillenews.org", "obn.ba", "observer.com", "globo.com", "ortb.bj", "ottawacitizen.com", "ottawasun.com", "ozzienews.com",
    "pbsguam.org", "peru.com", "pina.com.fj", "politiken.dk", "pridnestrovie-daily.net", "freepressjournal.in", "thequint.com",
    "punchng.com", "quintdaily.com", "rabble.ca", "rightwirereport.com", "sueddeutsche.de", "idnes.cz", "shabait.com", "sic.pt",
    "sloveniatimes.com", "sltn.co.uk", "sluggerotoole.com", "smallwarsjournal.com", "soranews24.com", "southeastasiaglobe.com",
    "sme.sk", "splash247.com", "standforfreedom.ca", "starofmysore.com", "startupreporter.in", "abc.es", "stcroixsource.com", 
    "sudantribune.com", "thechinaproject.com", "tribunnews.com", "surgezirc.co.uk", "talkingupscotlandtwo.com", "taz.de",
    "technode.com", "thebridge.jp", "thediplomat.com", "thefrontierpost.com", "thegambiaradio.com", "theintercept.com",
    "theiranproject.com", "thenassauguardian.com", "thenewdawnliberia.com", "thenewshimachal.com", "theorkneynews.scot",
    "theparisnews.com", "theprovince.com", "thestandard.org.nz", "thestarphoenix.com", "tibettimes.net", "ticotimes.net",
    "tiempo.hn", "times.mw", "indiatimes.com", "togopresse.tg", "citynews.ca", "torontosun.com", "uacrisis.org", "urbana.com.py",
    "uscnpm.org", "vancouversun.com", "vanguardia.com.mx", "vecer.mk", "villagemagazine.ie", "vladnews.ru", "vob929.com",
    "voxeurop.eu", "wan-ifra.org", "warontherocks.com", "warritatafo.com", "whdh.com", "gazeta.pl", "windsorstar.com", "wsvn.com",
    "24chasa.bg", "24-horas.mx", "24sata.hr", "abbynews.com", "abc.net.au", "acap.cf", "adworld.ie", "aftenposten.no",
    "agassizharrisonobserver.com", "agriland.ie", "aib.media", "alalam.ma", "albayan.ae", "albayan.aehttps", "aletihad.ae",
    "altoadige.it", "amnesty.org", "aninews.in", "anphoblacht.com", "apnlive.com", "artscouncil.ie", "asianexpress.co.uk",
    "asiasentinel.com", "autonews.com", "northernirelandworld.com", "belfastlive.co.uk", "bhaskarlive.in", "bhutannewsservice.org",
    "bordertelegraph.com", "boston.com", "bostonherald.com", "breakingnewstoday.co.uk", "brookings.edu", "buchanobserver.co.uk",
    "budapesttimes.hu", "business-standard.com", "campaignasia.com", "canberratimes.com.au", "capital.bg", "capitalqueretaro.com.mx",
    "osvnews.com", "cbsnews.com", "ceskenoviny.cz", "challenge.ma", "chanarcillo.cl", "chicagotribune.com", "chinaentertainmentnews.com",
    "chosonsinbo.com", "churchofscotland.org.uk", "thecjn.ca", "cnbc.com", "computerworld.com", "costa-news.com", "cricketireland.ie",
    "crtv.cm", "ctitv.com.tw", "cubanet.org", "dailyexcelsior.com", "dailyherald.com", "dailyheraldtribune.com", "dailynews.co.th",
    "dailypolitics.com", "dailypost.vu", "dailyrecord.co.uk", "danas.rs", "dayniiile.com", "dbsuriname.com", "deadlinenews.co.uk",
    "debate.com.mx", "deccanchronicle.com", "delfi.lv", "derryjournal.com", "deutschland.de", "diariocolatino.com", "gouv.fr?xtor=RSS-1",
    "dnaindia.com", "dnevnik.bg", "dnevnik.si", "donegaldaily.com", "dv.is", "eastasiaforum.org", "easternherald.com", "scotsman.com",
    "efe.com", "egyptindependent.com", "elcorreo.com", "eldiario.com.co", "eldiario.net", "elfinanciero.com.mx", "elnorte.com", 
    "elsiglodetorreon.com.mx", "eluniversal.com.mx", "el-universal.com", "emirates247.com", "ena.et", "esmitv.com", "europeantimes.news",
    "expatica.com", "fanabc.com", "faz.net", "financeasia.com", "firstpostofindia.com", "fleet.ie", "france24.com", "francetvinfo.fr",
    "ft.com", "glasgowlive.co.uk", "glasgowtimes.co.uk", "globes.co.il", "gnlm.com.mm", "goulburnpost.com.au", "atom.xml", "gov.br",
    "grampianonline.co.uk", "grenadabroadcast.com", "grimsbytelegraph.co.uk", "gs.by", "handelsblatt.com", "headlinesoftoday.com",
    "helsinkitimes.fi", "heraldscotland.com", "hoy.es", "huffpost.com", "iaasiaonline.com", "ibtimes.com.au", "ilmattino.it", 
    "ilmessaggero.it", "ilsole24ore.com", "iltalehti.fi", "iltempo.it", "independent.ie", "indiatoday.in", "inform.kz",
    "informador.mx", "insider.co.uk", "interfax.ru", "inverness-courier.co.uk", "iraqhurr.org", "irish-boxing.com",
    "irishbuildingmagazine.ie", "irishcentral.com", "irishmirror.ie", "irishtimes.com", "islandsun.com", "itnnews.lk",
    "ittefaq.com.bd", "iwacu-burundi.org", "iwnsvg.com", "japantimes.co.jp", "jasarat.com", "jornada.com.mx", 
    "journaldutogo.com", "jurnal.md", "kaieteurnewsonline.com", "kanivatonga.co.nz", "kbc.co.ke", "kentnews.online",
    "kilkennypeople.ie", "kiwikidsnews.co.nz", "kuwaittimes.com", "lacittadisalerno.it", "la-croix.com", "lahora.com.ec",
    "lanacion.cl", "lanation.dj", "lankabusinessonline.com", "laprensagrafica.com", "latimes.com", "latribune.fr", "laweekly.com",
    "lemonde.fr", "liberoquotidiano.it", "libertas.sm", "libertatea.ro", "limerickleader.ie", "lusakavoice.com", "macleans.ca",
    "madagascar-tribune.com", "majorcadailybulletin.com", "mbl.is", "meanwhileinireland.com", "mediapart.fr", "mediareform.org.uk",
    "mercurynews.com", "middleeastmonitor.com", "minnpost.com", "monde-diplomatique.fr", "mwnation.com", "naftemporiki.gr",
    "naharnet.com", "nationalobserver.com", "navhindtimes.in", "nbcchicago.com", "nbcmiami.com", "nbcwashington.com", "necn.com",
    "nepalitimes.com", "neweurope.eu", "news.lk", "newsagencyblog.com.au", "newsrust.com", "notiziegeopolitiche.net",
    "novamakedonija.com.mk", "novilist.hr", "novinite.com", "ntv.ru", "nv-online.info", "nyasatimes.com", "nytimes.com",
    "oneindia.com", "onlanka.com", "orissapost.com", "timeschronicle.ca", "ouestribune-dz.com", "owensoundsuntimes.com",
    "ozodi.org", "pakistantoday.com.pk", "peachlandview.com", "pembrokeobserver.com", "perthnow.com.au", "phillyvoice.com",
    "phnompenhpost.com", "thepinknews.com", "politico.eu", "politics.co.uk", "popularmyanmar.com", "positive.news", 
    "powersportz.tv", "premiumtimesng.com", "prensa-latina.cu", "prensalibre.com", "pressandjournal.co.uk", "theworld.org",
    "publimetro.com.mx", "publishedreporter.com", "radiohc.cu", "radiondekeluka.org", "rand.org", "rappler.com", "rawstory.com",
    "razon.com.mx", "reforma.com", "repubblica.it", "retailnews.asia", "rfa.org", "rfi.fr", "rm.co.mz", "rsvplive.ie", "rtb.bf",
    "rtrs.tv", "rts.rs", "rttlep.tl", "saanichnews.com", "sabcnews.com", "saipantribune.com", "salon.com", "sbs.com.au", "scmp.com",
    "scoop.co.nz", "scottishfield.co.uk", "shetlandtimes.co.uk", "sibconline.com.sb", "sidwaya.info", "sinceindependence.com",
    "sn.at", "solomonstarnews.com", "euronews247.com", "spiegel.de", "sta.si", "stluciamirroronline.com", "capsula.sa", "straight.com",
    "stratfordbeaconherald.com", "sudquotidien.sn", "sundaypost.com", "svd.se", "tagesschau.de", "tahitinews.co", "techgenyz.com",
    "telegraaf.nl", "telegraph.co.uk", "teluguglobal.com", "tempo.com.ph", "tentaran.com", "the42.ie", "theage.com.au",
    "theargus.co.uk", "theboltonnews.co.uk", "thecourier.co.uk", "thedailymash.co.uk", "thedailyscrumnews.com", "theflorentine.net",
    "thefridaytimes.com", "the-gazette.co.uk", "theguardian.com", "thejc.com", "thejournal.ie", "theleader.info",
    "themontserratreporter.com", "thenationalherald.com", "thenews.mx", "thenorthernecho.co.uk", "thenorthlines.com",
    "theolivepress.es", "thepoke.com", "thescarboroughnews.co.uk", "theseasidegazette.com", "thestkittsnevisobserver.com",
    "thetimesofbengal.com", "theyucatantimes.com", "thisdaylive.com", "times.co.nz", "timpul.md", "topky.sk", "tvm.co.mz",
    "twincities.com", "utusan.com.my", "vaticannews.va", "vecernji.hr", "vg.no", "vicnews.com", "vijesti.me", "vikalpa.org",
    "virakesari.lk", "volksblatt.li", "watchdoguganda.com", "wort.lu", "woxx.lu", "wprost.pl", "yabiladi.com", "yahoo.com",
    "yorkpress.co.uk", "youtube.com", "ziaruldeiasi.ro", "zlv.lu", "euobserver.com", "znsbahamas.com", "welt.de", "focus.de",
    "bild.de", "wissenschaft.de", "spektrum.de", "forschung-und-wissen.de", "reddit.com", "kyivpost.com", "theepochtimes.com",
    "dailywire.com", "thedispatch.com", "reason.com", "reuters.com", "hurriyet.com.tr", "yenisafak.com", "internethaber.com",
    "rferl.org", "haaretz.com", "sport.ua", "isport.ua"]


    # Check which categories are selected
    for category in categories:
        if request.form.get(category): # If the category is selected
            if selected_categories == "":
                selected_categories += category
            else:
                selected_categories += ',' + category
    # If no categories are selected
    if categories == "":
        return "No categories selected"
    
    # If no sources are selected
    if not selected_sources:
        return "No sources selected"
    
    selected_sources = ['https://www.' + item for item in selected_sources]
    # Making a string separated by commas from a list
    # according to API docs
    selected_sources = ','.join(selected_sources)
    # return selected_sources


    params = {
        'categories': selected_categories,
        'language': 'en',
        'number': 10,
        'news-sources': selected_sources
    }

    headers = {
        'x-api-key': api_key
    }

    # Make the request to the API
    response = requests.get(api_url, params=params, headers=headers)
    if response.status_code == 200:
        return response.json()

    return response.status_code
