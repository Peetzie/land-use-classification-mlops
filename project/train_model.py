from omegaconf import OmegaConf
import hydra


@hydra.main(config_name="configs/basic.yaml")
def main(cfg):
    print(cfg.configs.hyperparameters.batch_size, cfg.configs.hyperparameters.learning_rate)


if __name__ == "__main__":
    main()
