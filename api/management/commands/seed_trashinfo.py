from django.core.management.base import BaseCommand
from api.models import TrashInfo

class Command(BaseCommand):
    help = 'Seed data untuk tabel TrashInfo'

    def handle(self, *args, **kwargs):
        data = [
            {
                "label": "sampah-organik",
                "danger_level": "Rendah",
                "mitigation": "Komposing: Konversi menjadi pupuk organik, Biogas: Pengolahan anaerobik untuk menghasilkan energi, Pemilahan di sumber untuk mengurangi kontaminasi dengan sampah lain",
                "description": "Mudah terurai secara alami (biodegradable) melalui proses mikrobiologis, Tidak mengandung bahan toksik, tetapi dapat menghasilkan gas metana (CH₄) jika terdekomposisi anaerobik, Dampak utama adalah bau dan potensi pencemaran air jika tidak dikelola dengan baik"

            },
            {
                "label": "sampah-anorganik",
                "danger_level": "Sedang",
                "mitigation": "Daur ulang mekanis untuk plastik, kaca, dan logam, Reduksi penggunaan melalui kebijakan single-use plastic bans, Teknologi waste-to-energy untuk sampah non-recyclable",
                "description": "Tidak terurai secara alami (plastik butuh 20–500 tahun untuk terurai), Mikroplastik dapat masuk ke rantai makanan dan ekosistem perairan, Dapat menyebabkan penyumbatan saluran air dan kerusakan habitat."
            },
            {
                "label": "sampah-B3",
                "danger_level": "Tinggi",
                "mitigation": "Insinerasi suhu tinggi dengan scrubber untuk mengurangi emisi, Stabilisasi/solidifikasi untuk limbah logam berat, Koleksi terpisah dan labelisasi jelas",
                "description": "Mengandung logam berat (merkuri, kadmium), bahan kimia korosif, atau zat karsinogenik, Toksisitas akut/kronis bagi manusia dan ekosistem, Bioakumulasi dalam rantai makanan."
            },
            {
                "label": "sampah-Elektronik",
                "danger_level": "Tinggi",
                "mitigation": "Urban mining (ekstraksi logam berharga seperti emas/tembaga), Extended Producer Responsibility (EPR), Teknologi daur ulang ramah lingkungan",
                "description": "Kandungan logam berat (timbal, merkuri) dan bahan halogenated (BFRs) yang bersifat persistensi, Pencemaran tanah dan air melalui lindi, Efek kesehatan: Gangguan saraf dan reproduksi"
            },
            
        ]

        for item in data:
            obj, created = TrashInfo.objects.update_or_create(
                label=item['label'],
                defaults={
                    "danger_level": item["danger_level"],
                    "mitigation": item["mitigation"],
                    "description": item["description"]
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✔ Created: {item['label']}"))
            else:
                self.stdout.write(self.style.WARNING(f"➤ Updated: {item['label']}"))
