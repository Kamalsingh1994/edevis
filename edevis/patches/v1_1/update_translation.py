import frappe

def execute():
    trans_keys = [
        "Liability text",
        "Copyright protection text",
        "Retention of title text",
        "Supply of spare parts text"
    ]

    frappe.db.delete("Translation", {
        "language": "en",
        "source_text": ["in", trans_keys]
    })

    frappe.db.delete("Translation", {
        "language": "de",
        "source_text": ["in", trans_keys]
    })

    translations_en = {
        "Liability text": "We are liable under our liability insurance for all damage culpably caused by us or our agents and assistants as follows: <br><ul><li>for property damage up to 5,000,000.00 EUR</li><li>for personal injury under the statutory provisions</li></ul>Further claims for damages and liability for loss of production and loss of profit are excluded.",
        "Copyright protection text": "The text of the quotation, as well as all specification sheets, drawings, software, plans and other documents include a high degree of know-how, ideas and development services of edevis GmbH. All documents and information may not be copied, analysed be reproduced or given to third parties in any other way in whole or in part without permission. Also details of it are subject to legal protection. Exceptions require written approval by the edevis GmbH.",
        "Retention of title text": "The delivery is carried out exclusively under retention of title. The property shall not pass to the buyer if he/she has repaid all obligations arising from the agreements concluded between him/her and us. For current accounts, the retained goods count as security for our claims. If the parts are integrated into an existing system of the buyer, we will share ownership pro-rata of the entire system. The retention of title as well as the seizure of the goods by us shall not automatically constitute a withdrawal from the contract. If the buyer excesses a payment date, we are entitled to take back the object of our retention of title. At the conclusion of the contract, the buyer agrees in any action by us which are necessary to obtain the immediate possession of the object of the reservation.",
        "Supply of spare parts text": "Warranty period: 365 days*. The warranty period begins on the day of delivery and is independent of the operating time. Within this period we have the option of repairing a defective part free of charge or replacing it with a faultless one. We do not accept any liability for damage caused by the following reasons: unsuitable or improper use, tampering, assembly or commissioning by the purchaser or third parties, natural wear and tear or incorrect handling.<br><br>*with the exception of wearing parts (such as converters, boosters, sonotrodes, flash tubes, halogen lamps, laser diodes, etc.).",
    }

    translations_de = {
        "Liability text": "Wir haften im Rahmen unserer Haftpflichtversicherung für alle durch uns oder unsere Erfüllungs- und Verrichtungsgehilfen schuldhaft verursachten Schäden wie folgt:<br><ul><li>für Sach- und Vermögensschäden bis 5.000.000,00EUR</li><li>für Personenschäden gemäß der gesetzlichen Bestimmungen</li></ul>Weitere Schadensansprüche, insbesondere die Haftung für Produktionsausfall und entgangenem Gewinn, sind ausgeschlossen.",
        "Copyright protection text": "Der Angebotstext, sowie alle im Auftragsfall erstellten Pflichtenhefte, Zeichnungen, Software, Pläne und sonstigen Unterlagen beinhalten in hohem Maße Know-how, Ideen und Entwicklungsleistungen der Edevis GmbH. Alle Unterlagen und Informationen dürfen ohne die Erlaubnis von uns weder ganz noch auszugsweise kopiert, ausgewertet, vervielfältigt oder in irgendeiner anderen Weise Dritten zugänglich gemacht werden. Auch Einzelheiten daraus unterliegen den gesetzlichen Schutzbestimmungen. Ausnahmen hierzu bedürfen der schriftlichen Genehmigung durch die Edevis GmbH.",
        "Retention of title text": "Die Lieferung erfolgt ausschließlich unter Eigentumsvorbehalt. Das Eigentum geht erst dann auf den Käufer über, wenn dieser sämtliche Verbindlichkeiten aus den zwischen ihm und uns geschlossenen Verträgen getilgt hat. Bei laufender Rechnung gilt das vorbehaltene Eigentum als Sicherung unserer Forderungen. Sofern die Teile in eine beim Käufer vorhandene Anlage integriert werden, erhalten wir anteilmäßiges Miteigentum an der gesamten Anlage. Die Geltendmachung des Eigentumsvorbehalts sowie die Pfändung des Liefergegenstandes durch uns gilt nicht automatisch als Rücktritt vom Vertrag. Überschreitet der Käufer einen Zahlungstermin, so sind wir berechtigt, den Gegenstand unseres Eigentumsvorbehaltes zurückzunehmen. Der Käufer willigt bereits bei Abschluss des Vertrages in alle Handlungen durch uns ein, die zur Erlangung des unmittelbaren Besitzes des Gegenstandes des Eigentumsvorbehaltes notwendig sind.",
        "Supply of spare parts text": "Gewährleistungsfrist: 365 Tage*. Die Gewährleistungsfrist beginnt mit dem Tag der Lieferung und ist unabhängig von der Betriebsdauer. Innerhalb dieser Frist haben wir die Möglichkeit, ein defektes Teil kostenlos zu reparieren oder durch ein einwandfreies zu ersetzen. Wir übernehmen keine Haftung für Schäden, die aus folgenden Gründen entstanden sind: Ungeeignete oder unsachgemäße Verwendung, Eingriffe, Montage oder Inbetriebnahme durch den Käufer oder Dritte, natürliche Abnutzung oder fehlerhafte Behandlung.<br><br>*davon ausgenommen sind Verschleißteile (wie zum Beispiel Konverter, Booster, Sonotroden, Blitzröhren, Halogen-Leuchtmittel, Laserdioden, ...).",
    }

    for source, target in translations_en.items():
        frappe.get_doc({
            "doctype": "Translation",
            "language": "en",
            "source_text": source,
            "translated_text": target
        }).insert(ignore_if_duplicate=True)

    for source, target in translations_de.items():
        frappe.get_doc({
            "doctype": "Translation",
            "language": "de",
            "source_text": source,
            "translated_text": target
        }).insert(ignore_if_duplicate=True)

    frappe.db.commit()
