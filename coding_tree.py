from PDFReader import GetAllData
from site_scraper import *
from sqlstatements import *
from PDFReader import GetinfoPDF
import variables as v
import os


D_HumanCapital = { #TOTAAL: 96 termen
    'GENDERGELIJKHEID' : ['geslacht','gendergelijkheid','verhouding vrouw','ratio man/vrouw','salaris man/vrouw','discriminatie','genderneutraal'],
    'IMPLEMENTATIE WERKNEMERSRECHTEN' : ['duurzaamheidscommissie','rechten van werknemers','arbeidsrechten','rechten en plichten werknemers','arbeidsomstandigheden','rechten','plichten','mensenrechten','recht op vrijheid'],
    'SOCIALE RELATIES OP HET WERK' : ['sociale relaties','werkvloer','solidair gedrag','betrokkenheid van werknemers'],
    'WERKGELEGENHEID' : ['rekrutering','rekruteringsbeleid','rekruteringsverloop','rekruteringstijd','arbeidsovereenkomst','werknemer','werknemers','diversiteitsbeleid','loopbaan','carrière','carrièreontwikkeling','groei opportuniteiten','groeikansen','doorstroommogelijkheden','promotie','demografisch','personeelsbestand','promotie','human resources','HR','personeelsbeleid'],
    'ORGANISATIE OP HET WERK' : ['vergoeding', 'beloning', 'bonus', 'stabiliteit van werknemers', 'stabiliteit', 'bedrijfscultuur', 'loyaliteit van werknemers', 'personeelsbehoud', 'retentie personeel', 'loyaliteitsbonus', 'personeelsverloop', 'leeftijdsstructuur', 'afwezigheid', 'afwezigheidsratio', 'tevredenheid op het werk', 'opvolgingsbeheer', 'prestatiebeleid', 'prestatie', 'ziekte', 'verzuim', 'aanwezigheid', 'aanwezigheidsratio'],
    'GEZONDHEID EN VEILIGHEID' : ['preventie', 'pesterij', 'ongewenst gedrag', 'klacht', 'gezondheid van werknemers', 'welzijn van werknemers', 'managers', 'arbeiders', 'bedienden', 'medewerkers', 'incidenten op het werk', 'incidenten', 'discriminatie', 'gezondheid en veiligheid op het werk', 'intimidatie', 'intimiderend gedrag', 'vakbond' ],
    'OPLEIDINGSBELEID' : ['opleidingsbeleid', 'training', 'opleiding', 'vaardigheden van werknemers', 'kennis van werknemers werknemersvaardigheden', 'competenties van werknemer', 'werknemercompetenties', 'talent', 'vakbekwaamheid' ],
    'SDG' : ['kinderarbeid', 'goede gezondheid en welzijn', 'gender-gelijkheid', 'waardig werk en economische groei', 'ongelijkheid verminderen', 'vrede', 'veiligheid en sterke publieke diensten'],
}

D_NaturalCapital = { #TOTAAL: 70 termen
    'GEBRUIK VAN ENERGIEBRONNEN' : ['energiebron','energie vermindering', 'energie reductie', 'energie-intensiteit', 'energiegebruik', 'energieverbruik'],
    'GEBRUIK VAN WATERBRONNEN' : ['waterverbruik', 'waterbron', 'wateronttrekking', 'waterafvoer', 'watergebruik', 'afvalwater', 'grondwater' ],
    'EMISSIES VAN BROEIKASGASSEN' : ['broeikasgas', 'CO2', 'CO²', 'CO2'],
    'VERVUILENDE UITSTOOT' : ['emissie', 'uitstoot', 'vervuiling', 'zure regen', 'uitstoot', 'fijnstof', 'fijn stof', 'vervuilende stof', 'filtertechniek', 'luchtzuiverheid', 'zuiveringstechnologie'],
    'MILIEU-IMPACT' : ['impact', 'milieu-impact', 'impact op het milieu', 'milieu impact', 'milieu', 'mobiliteit', 'vervoer', 'verplaatsing', 'fiets', 'auto', 'staanplaatsen', 'parking', 'openbaar vervoer', 'klimaatimpact', 'impact op het klimaat', 'klimaatsverandering', 'green deal'],
    'IMPACT OP GEZONDHEID EN VEILIGHEID' : ['gezondheid', 'reclyclage', 'recycleren', 'biodiversiteit', 'afval', 'afvalproductie', 'vervuiling'],
    'VERDERE EISEN OVER BEPAALDE ONDERWERPEN' : ['klimaat', 'klimaatsverandering', 'klimaatopwarming', 'opwarming', 'scope'],
    'MILIEU BELEID' : ['milieubeleid', 'hernieuwbare energie', 'verspilling', 'milieucriteria', 'planeet', 'klimaatsbeleid', 'milieunormen'],
    'SDG' : ['schoon water en sanitair', 'betaalbare en duurzame energie', 'duurzame steden en gemeenschappen', 'verantwoorde consumptie en productie', 'klimaatactie, leven in het water', 'leven op het land']
}
                          
def counterHumanCapital(text_site, inhoudpdf):
    counterTermen = 0 #counter voor termen per domein
    pdfCounter = 0
    siteCounter = 0
    res_codingTree = []
    for Rapporteringsdomeinen, opzoektermen in D_HumanCapital.items():       
        res_codingTree.append(Rapporteringsdomeinen)
        for term in opzoektermen:
            if term in inhoudpdf:
                counterTermen += 1
                pdfCounter +=1 
            if term in text_site: 
               counterTermen += 1
               siteCounter += 1 
        res_codingTree.append(counterTermen)
        res_codingTree.append(localiseerZoekterm(siteCounter,pdfCounter))
        siteCounter = 0
        pdfCounter = 0
        counterTermen = 0 
    return res_codingTree


def counterNaturalCapital(text_site, inhoudpdf):
    counterTermen = 0 #counter voor termen per domein
    pdfCounter = 0
    siteCounter = 0
    res_codingTree = []
    for Rapporteringsdomeinen, opzoektermen in D_NaturalCapital.items():
        res_codingTree.append(Rapporteringsdomeinen)
        for term in opzoektermen:
            if term in inhoudpdf:
                counterTermen += 1
                pdfCounter += 1
            if term in text_site:
                counterTermen += 1
                siteCounter += 1
        res_codingTree.append(counterTermen)
        res_codingTree.append(localiseerZoekterm(siteCounter,pdfCounter))
        siteCounter = 0
        pdfCounter = 0
        counterTermen = 0
    return res_codingTree

def localiseerZoekterm(siteCounter, pdfCounter):
    score = 0
    if pdfCounter == 0 and siteCounter > 0:
        score = 1
    elif pdfCounter > 0 and siteCounter == 0:
        score = 2
    elif pdfCounter > 0 and siteCounter > 0:
        score = 3
    return score



def duurzaamheidsScore(h,n):
    TOTAAL_AANTAL_TERMEN = 166
    totaalcounter=h[1] + h[4] + h[7] + h[10] + h[13] + h[16] + h[19] + h[22] 
    + n[1] + n[4] + n[7] + n[10]+ n[13] + n[16] + n[19] + n[22] + n[25]
    letter = "D"
    score = (TOTAAL_AANTAL_TERMEN-totaalcounter)/TOTAAL_AANTAL_TERMEN
    if score<= 0.25:
         letter = "A"
    elif score<=0.50:
         letter = "B"
    elif score<=0.75:
         letter = "C"
    return letter,score

def main():
    # --- SITES --- 
    l_nr_bedrijven = getBedrijvennummerMetSite()
    l_sites_bedrijven = []
    
    # --- PDF's ---
    l_pdfs_bedrijven = []
    ONEDRIVE_LOCATIE = v.onedrive
    bedrijven = os.listdir(ONEDRIVE_LOCATIE)
    for bedrijf in bedrijven:
        for nummer in l_nr_bedrijven:
            l_sites_bedrijven.append(getSitesBedrijven(nummer)) 
            fileloc = ONEDRIVE_LOCATIE+bedrijf
            bedrijfsnummer=""
            for char in bedrijf:
                if char.isdigit():
                    bedrijfsnummer+=str(char)
        l_pdfs_bedrijven.append(GetinfoPDF(fileloc))
        print(l_pdfs_bedrijven)

    for site, pdf in zip(l_sites_bedrijven, l_pdfs_bedrijven):
        text_site = get_text(site)
        inhoudPDF = pdf       
        inhoudPDF = [i.lower() for i in inhoudPDF]

        res_codingTree_h = counterHumanCapital(text_site, inhoudPDF) 
        res_codingTree_n = counterNaturalCapital(text_site, inhoudPDF)          
        duurzaamheidsscore = duurzaamheidsScore(res_codingTree_h, res_codingTree_n)
        #setBedrijfCodingTree(nummer,res_codingTree_h[2],res_codingTree_n[2], score_zoekterm,duurzaamheidsscore)

     

if __name__ == "__main__":    
    main()

