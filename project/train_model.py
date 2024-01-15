from omegaconf import OmegaConf
import hydra


@hydra.main(config_name="configs/basic.yaml")
def main(cfg):
    print(cfg.hyperparameters.batch_size, cfg.hyperparameters.learning_rate)


if __name__ == "__main__":
    main()
