# Wikipedia Country Data Scraper

Ce script Python permet de faire du web scraping des données de pays depuis Wikipedia.

## 📊 Données collectées

1. **Population** - Liste des pays par population
2. **PIB** - Liste des pays par PIB nominal
3. **Espérance de vie** - Liste des pays par espérance de vie

## 🚀 Installation

### 1. Installer Python
Assurez-vous d'avoir Python 3.7+ installé sur votre système.

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

Ou installez les packages individuellement:
```bash
pip install requests beautifulsoup4 pandas openpyxl lxml
```

## 💻 Utilisation

### Utilisation basique
```python
python wikipedia_scraper.py
```

### Utilisation avancée dans votre code

```python
from wikipedia_scraper import WikipediaScraper

# Créer une instance du scraper
scraper = WikipediaScraper()

# Scraper toutes les données et sauvegarder
data = scraper.scrape_all(save_to_csv=True, save_to_excel=True)

# Ou scraper individuellement
df_population = scraper.scrape_population()
df_gdp = scraper.scrape_gdp()
df_life_expectancy = scraper.scrape_life_expectancy()

# Accéder aux données
population_df = data['population']
gdp_df = data['gdp']
life_expectancy_df = data['life_expectancy']

# Faire des analyses
print(population_df.head(10))
print(gdp_df.describe())
```

## 📁 Fichiers de sortie

Le script génère automatiquement:

### Fichiers CSV (individuels)
- `population_data.csv` - Données de population
- `gdp_data.csv` - Données de PIB
- `life_expectancy_data.csv` - Données d'espérance de vie

### Fichier Excel (consolidé)
- `countries_data.xlsx` - Toutes les données dans un seul fichier avec 3 feuilles

## 📋 Structure des données

### Population
- Rank (Rang)
- Country (Pays)
- Population

### GDP
- Rank (Rang)
- Country (Pays)
- GDP (USD millions)

### Life Expectancy
- Country (Pays)
- Life Expectancy (Overall)
- Life Expectancy (Male)
- Life Expectancy (Female)

## 🔧 Personnalisation

### Changer le nombre de pays
Modifiez la limite dans les fonctions de scraping:
```python
rows = table.find_all('tr')[1:51]  # Top 50 pays
```

### Ajouter d'autres champs
Ajoutez des colonnes supplémentaires en analysant plus de `cols`:
```python
additional_field = self.clean_text(cols[4].get_text())
```

### Exporter vers d'autres formats
```python
# JSON
df.to_json('data.json', orient='records', indent=2)

# Markdown
df.to_markdown('data.md', index=False)

# HTML
df.to_html('data.html', index=False)
```

## ⚠️ Notes importantes

1. **Respect des conditions d'utilisation**: Ce script respecte les conditions de Wikipedia
2. **Rate limiting**: Des délais sont inclus pour ne pas surcharger les serveurs
3. **User-Agent**: Un User-Agent est défini pour identifier les requêtes
4. **Gestion des erreurs**: Le script gère les erreurs de connexion et de parsing

## 🐛 Dépannage

### Erreur de connexion
```python
requests.exceptions.ConnectionError
```
- Vérifiez votre connexion internet
- Vérifiez que Wikipedia est accessible

### Erreur de parsing
```python
AttributeError: 'NoneType' object has no attribute 'find_all'
```
- La structure de la page Wikipedia a peut-être changé
- Vérifiez les sélecteurs de table dans le code

### Données manquantes
- Certaines cellules peuvent être vides sur Wikipedia
- Le script gère ces cas avec des try/except

## 📚 Ressources

- [Documentation BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Documentation Pandas](https://pandas.pydata.org/docs/)
- [Documentation Requests](https://requests.readthedocs.io/)

## 📄 Licence

Ce script est fourni à des fins éducatives. Respectez les conditions d'utilisation de Wikipedia.

## 🤝 Contribution

N'hésitez pas à améliorer ce script et à partager vos modifications!
