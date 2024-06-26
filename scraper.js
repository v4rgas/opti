const puppeteer = require('puppeteer');
const { createObjectCsvWriter } = require('csv-writer');

const stringId2Id = (stringId) => {
    return parseInt(stringId.replace(/[^0-9.]/g, ""));
};

const loadPage = async (page, url) => {
    await page.goto(url);
    console.log("Page loaded");
};

const loadProvincesDPAs = async (page) => {
    await page.evaluate(() => {
        fJquery.cargarSliderDPA();
    });
    await page.waitForSelector("#contenidoDpa_provincia", { visible: true });
    await page.evaluate(() => {
        document.querySelector("#contenidoDpa_provincia").click();
    });
    await page.waitForSelector("#elementosTable_provincia", { visible: true });
    console.log("Provinces loaded");
};

const getProvinces = async (page) => {
    let provinces =  await page.evaluate(() => {
        const provinceElements = document.querySelectorAll("#elementosTable_provincia li");
        console.log(provinceElements);
        return Array.from(provinceElements).map(provinceElement => {
            return {
                name: provinceElement.innerText,
                cssID: provinceElement.getAttribute("id")
            };
        });
    });
    provinces.forEach(province => {
        province.id = stringId2Id(province.cssID);
    });
    return provinces;
};

const getProvinceDetails = async (page, province) => {
    const provinceSelector = `[id^='${province.cssID}']`;
    console.log(provinceSelector);


    await page.waitForSelector("#elementosTable_provincia", { visible: true });

    await page.evaluate((selector) => {
        document.querySelector(selector).click();
    }, provinceSelector); // Click on the province

    await page.waitForSelector("#footer_solar");
    
    const solarPotential = await page.evaluate(() => {
        return document.querySelector("#footer_solar p span")?.innerText || "0 kWhr/m2";
    });

    const windPotential = await page.evaluate(() => {
        return document.querySelector("#footer_eolico p span")?.innerText || "0 m/s";
    });

    const hydroPotential = await page.evaluate(() => {
        return document.querySelector("#footer_hidro p span")?.innerText || "0 m3/s";
    });

    const area = await page.evaluate(() => {
        let stringArea = document.querySelector("#contnGeoReport > div:nth-child(2) > div > div.md-card-content.georeporte_graf.onlytxt > p:nth-child(4)").innerText;
        return stringArea.slice("Área: ".length).replace(/\./g, "").replace(/\,/g, ".");
    });

    const center = await page.evaluate(() => {
        let stringCenter =  document.querySelector("#contnGeoReport > div:nth-child(2) > div > div.md-card-content.georeporte_graf.onlytxt > p:nth-child(2)").innerText;
        return stringCenter.slice("Ubicación centroide: ".length).replace(/\,/g, "");
    });

    const potentials = {
        solar: solarPotential,
        wind: windPotential,
        hydro: hydroPotential
    };

    const details = {
        potentials: potentials,
        area: area,
        center: center
    };

    return details;
};

const getAllDetails = async () => {
    const browser = await puppeteer.launch({ headless: true }); // false to see the browser
    const page = await browser.newPage();

    // page.on("console", msg => console.log("PAGE LOG:", msg.text())); // Log the console messages

    await loadPage(page, "https://energiamaps.cne.cl/#");

    await loadProvincesDPAs(page);

    const provinces = await getProvinces(page);

    console.log(provinces); // Print the provinces

    let allDetails = [];
    for (let i = 0; i < provinces.length; i++) {
        const province = provinces[i];
        const details = await getProvinceDetails(page, province);
        allDetails.push({
            province: province.name,
            area: details.area,
            center: details.center,
            potentials: details.potentials,
        });
        console.log(province.name, details);
        await loadProvincesDPAs(page);
    };

    await browser.close();

    console.log(allDetails);
    return allDetails;
};

const AllDetails = getAllDetails();

AllDetails.then(async (details) => {
    const csvWriter = createObjectCsvWriter({
        path: "potencial_provincias.csv",
        header: [
            { id: "province", title: "PROVINCIA" },
            { id: "solar", title: "POTENCIAL SOLAR" },
            { id: "wind", title: "POTENCIAL EÓLICO" },
            { id: "hydro", title: "POTENCIAL HIDROELÉCTRICO" },
            { id: "area", title: "SUPERFICIE" },
            { id: "center", title: "CENTROIDE" }
        ]
    });

    const records = details.map(item => {
        return {
            province: item.province,
            solar: item.potentials.solar,
            wind: item.potentials.wind,
            hydro: item.potentials.hydro,
            area: item.area,
            center: item.center
        };
    });

    csvWriter.writeRecords(records).then(() => {
        console.log("CSV written");
    });
});