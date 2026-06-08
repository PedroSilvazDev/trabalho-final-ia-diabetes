from src.data_loader import download_dataset


if __name__ == "__main__":
    path = download_dataset()
    print(f"Dataset disponivel em: {path}")
