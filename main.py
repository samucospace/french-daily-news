import sys
import argparse
from src.news import fetch_latest_headlines
from src.llm import generate_newsletter_content
from src.mailer import send_daily_email

MOCK_CONTENT = {
    "greeting": "Chers passionnés de la langue française, voici l'essentiel de l'actualité mondiale décrypté avec rigueur et élégance stylistique.",
    "news_items": [
        {
            "title_fr": "Sommet sur le climat : Les négociations achoppent sur le financement de la transition",
            "summary_fr": "Alors que les délégations internationales peinent à s'accorder sur des engagements contraignants, plusieurs pays émergents fustigent l'inertie des puissances industrielles. Nonobstant les déclarations d'intention, le fossé financier demeure béant.",
            "source": "Le Monde"
        },
        {
            "title_fr": "Avancées majeures dans l'informatique quantique : Entre enthousiasme et précautions éthiques",
            "summary_fr": "Une coalition de chercheurs européens a dévoilé un processeur supraconducteur surpassant les limites antérieures. Quoique prometteuse, cette percée soulève des inquiétudes quant à la vulnérabilité des protocoles cryptographiques contemporains.",
            "source": "France 24"
        }
    ],
    "vocabulary": [
        {
            "term": "l'achoppement (m.)",
            "definition_fr": "Difficulté ou obstacle sur lequel bute une négociation ou une entreprise.",
            "translation_en": "stumbling block / impediment",
            "example_sentence": "Le partage des coûts d'infrastructure constitue le principal point d'achoppement entre les deux ministères."
        },
        {
            "term": "nonobstant (prép.)",
            "definition_fr": "Sans tenir compte de, malgré (terme soutenu et juridique).",
            "translation_en": "notwithstanding / despite",
            "example_sentence": "Nonobstant les réserves émises par les experts, le projet de loi a été adopté à une courte majorité."
        },
        {
            "term": "béant, -e (adj.)",
            "definition_fr": "Grand ouvert ; par extension figurée : immense, vertigineux.",
            "translation_en": "gaping / wide open",
            "example_sentence": "Le fossé générationnel semble plus béant que jamais au sein de l'organisation."
        }
    ],
    "lesson_of_the_day": {
        "topic": "La nuance stylistique : 'Quoique' suivi du subjonctif vs 'Bien que'",
        "paragraph": "En français soutenu, la locution conjonctive 'quoique' s'emploie couramment pour introduire une concession tout en allégeant le style par rapport à la répétition fréquente de 'bien que'. Attention à ne pas confondre l'orthographe en un seul mot ('quoique', signifiant 'bien que') avec la locution en deux mots ('quoi que', signifiant 'quelle que soit la chose qui'). Par exemple : 'Quoiqu'il soit (un mot) tard, il poursuit ses travaux' vs 'Quoi qu'il dise (deux mots), restez impassible'."
    },
    "challenge": {
        "question": "Complétez avec 'quoique' ou 'quoi que' : '_____ vous fassiez, veillez à respecter les préceptes académiques, _____ la tâche puisse vous paraître ardue.'",
        "answer": "1. 'Quoi que' (en deux mots, car remplaçable par 'quelle que soit la chose que vous fassiez'). 2. 'quoique' (en un seul mot, signifiant 'bien que')."
    }
}

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = argparse.ArgumentParser(description="French Daily News & Lesson Email Dispatcher")
    parser.add_argument("--preview", action="store_true", help="Generate and save HTML to preview.html without sending")
    parser.add_argument("--mock", action="store_true", help="Use mock content instead of calling OpenRouter (useful for dry runs)")
    parser.add_argument("--output", type=str, default="preview.html", help="Path to save preview HTML file")
    args = parser.parse_args()

    print("=== Démarrage de la Gazette Quotidienne ===")

    if args.mock:
        print("[Mode Mock] Utilisation du contenu de test pré-généré...")
        content = MOCK_CONTENT
    else:
        print("1. Récupération des dernières dépêches internationales (flux RSS)...")
        articles = fetch_latest_headlines(max_items=8)
        if not articles:
            print("[Erreur] Impossible de récupérer les actualités RSS.")
            sys.exit(1)
        print(f"   -> {len(articles)} articles récupérés avec succès.")

        print("2. Génération de l'édition et de la leçon avancée via OpenRouter...")
        content = generate_newsletter_content(articles)

    preview_path = args.output if args.preview else None
    
    print("3. Rendu et distribution de l'e-mail...")
    send_daily_email(content, preview_file=preview_path, preview_only=args.preview)
    print("=== Opération terminée avec succès ! ===")

if __name__ == "__main__":
    main()
