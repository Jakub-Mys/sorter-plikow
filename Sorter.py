import shutil
import hashlib
from pathlib import Path

CATEGORIES = {
    "Obrazki": ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    "Dokumenty": ['.pdf', '.doc', '.docx', '.txt', '.xls', '.xlsx', '.ppt', '.pptx', '.csv'],
    "Instalatory": ['.exe', '.msi'],
    "Archiwa": ['.zip', '.rar', '.7z', '.tar', '.gz'],
    "Wideo": ['.mp4', '.mkv', '.avi', '.mov'],
    "Muzyka": ['.mp3', '.wav', '.flac']
}

EXTENSION_MAP = {ext: folder for folder, exts in CATEGORIES.items() for ext in exts}


def get_file_hash(filepath: Path, chunk_size: int = 8192) -> str | None:
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            while chunk := f.read(chunk_size):
                hasher.update(chunk)
        return hasher.hexdigest()
    except OSError as e:
        print(f"Błąd odczytu pliku {filepath}: {e}")
        return None


def organize_and_deduplicate(source_dir: Path) -> None:
    if not source_dir.exists():
        print(f"Błąd: Nie znaleziono folderu {source_dir}")
        return

    moved_count = 0
    duplicate_count = 0

    print(f"Skanowanie i porządkowanie w: {source_dir}...\n")

    quarantine_dir = source_dir / "Kwarantanna"
    quarantine_dir.mkdir(exist_ok=True)

    for item in source_dir.iterdir():
        if item.is_dir():
            continue

        if item.is_file():
            file_ext = item.suffix.lower()
            target_folder_name = EXTENSION_MAP.get(file_ext, "Inne")
            target_dir = source_dir / target_folder_name

            target_dir.mkdir(exist_ok=True)

            item_size = item.stat().st_size
            is_duplicate = False
            item_hash = None
            duplicate_of = ""

            for existing_file in target_dir.iterdir():
                if existing_file.is_file() and existing_file.stat().st_size == item_size:
                    if item_hash is None:
                        item_hash = get_file_hash(item)

                    existing_hash = get_file_hash(existing_file)

                    if item_hash and existing_hash and item_hash == existing_hash:
                        is_duplicate = True
                        duplicate_of = existing_file.name
                        break

            if is_duplicate:
                quarantine_filename = item.name
                quarantine_path = quarantine_dir / quarantine_filename

                counter = 1
                while quarantine_path.exists():
                    quarantine_filename = f"{item.stem}_{counter}{item.suffix}"
                    quarantine_path = quarantine_dir / quarantine_filename
                    counter += 1

                try:
                    shutil.move(str(item), str(quarantine_path))
                    print(f"Przeniesiono do kwarantanny: {item.name} (identyczny z: {duplicate_of})")
                    duplicate_count += 1
                    continue
                except OSError as e:
                    print(f"Błąd podczas przenoszenia do folderu kwarantanna {item.name}: {e}")
                    continue

            new_filename = item.name
            target_path = target_dir / new_filename

            counter = 1
            while target_path.exists():
                new_filename = f"{item.stem}_{counter}{item.suffix}"
                target_path = target_dir / new_filename
                counter += 1

            try:
                shutil.move(str(item), str(target_path))
                print(f"Przeniesiono: {item.name} -> {target_folder_name}/{new_filename}")
                moved_count += 1
            except OSError as e:
                print(f"Błąd podczas przenoszenia {item.name}: {e}")

    print(f"\nGotowe! Posprzątano {moved_count} plików, przeniesiono do kwarantanny {duplicate_count} duplikatów.")


if __name__ == "__main__":
    downloads_path = Path.home() / "Downloads"
    organize_and_deduplicate(downloads_path)