from src.log.guardians.app.features.chunking.chunker import load_config, chunk_log_file


def main():
    config = load_config('config/chunker_config.yaml')
    chunk_log_file(config)


if __name__ == "__main__":
    main()