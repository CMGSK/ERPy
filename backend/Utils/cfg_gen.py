# from Operations import Configurations
def generate_from_db():
    cfg_params = []  # Select all from configs where to_env == true
    with open('../.cfg/.env', 'w') as env:
        for cfg in cfg_params:
            env.write(f'{cfg['conf_var'].upper()}={cfg['value']}')
