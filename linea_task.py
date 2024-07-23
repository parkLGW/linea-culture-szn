import asyncio
import random

from loguru import logger
from clutchplay import ClutchPlay
from nft_mint import NFTMint
from phosphor import Phosphor
from fake_useragent import UserAgent


class Linea:
    def __init__(self, idx, private_key, user_agent, proxy=None):
        self.idx = idx
        self.proxy = proxy
        self.linea_rpc = 'https://rpc.linea.build'
        self.proxies = {
            "http": f"socks5://{proxy}",
            "https": f"socks5://{proxy}"
        }
        self.clutch_ai = ClutchPlay(idx, private_key, user_agent, self.linea_rpc, self.proxies)
        self.nft_mint = NFTMint(idx, private_key, self.linea_rpc, self.proxies)
        self.phosphor = Phosphor(idx, private_key, user_agent, self.linea_rpc, self.proxies)

    async def mint_efrogs_quest(self):
        await self.nft_mint.mint_on_nfts2me('efrogs')
        logger.success(f"account {self.idx} complete 【W1:eFrogs】 success ✅")

    async def mint_wizards_quest(self):
        await self.nft_mint.mint_on_nfts2me('wizards')
        logger.success(f"account {self.idx} complete 【W1:Wizards of Linea】 success ✅")

    async def mint_linus_egg_quest(self):
        await self.nft_mint.mint_on_element('element', '0x1ffca9db')
        logger.success(f"account {self.idx} complete 【W2:Linus】 success ✅")

    async def mint_yooldo_quest(self):
        await self.nft_mint.mint_yooldo_nft()
        logger.success(f"account {self.idx} complete 【W2:Yooldo】 success ✅")

    async def mint_frog_wars_quest(self):
        await self.nft_mint.mint_on_nfts2me('frog_wars')
        logger.success(f"account {self.idx} complete 【W2:Frog Wars】 success ✅")

    async def mint_acg_quest(self):
        await self.nft_mint.mint_acg_nft()
        logger.success(f"account {self.idx} complete 【W2:ACG】 success ✅")

    async def mint_toad_quest(self):
        await self.nft_mint.mint_on_nfts2me('toad')
        logger.success(f"account {self.idx} complete 【W2:Toad The Great】 success ✅")

    async def mint_ascend_the_end_quest(self):
        await self.nft_mint.mint_on_element('element', '0x19a747c1')
        logger.success(f"account {self.idx} complete 【W3:AscendTheEnd】 success ✅")

    async def mint_sending_me_quest(self):
        await self.nft_mint.mint_sending_me_nft()
        logger.success(f"account {self.idx} complete 【W3:SendingMe】 success ✅")

    async def mint_town_story_quest(self):
        await self.nft_mint.mint_on_nfts2me('town_story')
        logger.success(f"account {self.idx} complete 【W3:Townstory】 success ✅")

    async def mint_danielle_quest(self):
        await self.nft_mint.mint_on_nfts2me('danielle_zosavac')
        logger.success(f"account {self.idx} complete 【W3:DanielleZosavac】 success ✅")

    async def mint_demmortal_treasure_quest(self):
        await self.nft_mint.mint_on_nfts2me('demmortal_treasure')
        logger.success(f"account {self.idx} complete 【W3:Demmortal Treasure】 success ✅")

    async def mint_foxy_quest(self):
        await self.nft_mint.mint_on_element('element', '0x2968bd75')
        logger.success(f"account {self.idx} complete 【W3:Foxy】 success ✅")

    async def clutch_quest(self):
        await self.clutch_ai.login()
        campaign_data = await self.clutch_ai.get_campaigns_data()

        campaign_id = campaign_data['id']
        model_id = campaign_data['model_ids'][0]

        await self.clutch_ai.generate(model_id, campaign_id)
        await asyncio.sleep(random.randint(20, 30))

        try_times = 3
        while True:
            if try_times == 0:
                raise Exception(f'account {self.idx} generate image failed❌')
            collections = await self.clutch_ai.get_collections()
            if collections is not None and len(collections) > 0 and collections[0]['campaign_id'] == campaign_id:
                break
            await asyncio.sleep(30)
            logger.info(f'account {self.idx} wait for collection...')
            try_times -= 1

        image_url = collections[0]['image_url']
        collection_id = collections[0]['id']
        ipfs_url = await self.clutch_ai.upload_img(image_url, collection_id)
        await self.clutch_ai.mint_clutch_ai_nft(ipfs_url, collection_id)

        logger.success(f"account {self.idx} complete 【W1:Crazy Gang】 success ✅")

    async def coop_records_quest(self):
        await self.phosphor.purchase_intents()
        logger.success(f"account {self.idx} complete 【W4:Coop Records】 success ✅")


async def start_linea_l3_quest(semaphore, mission_type, idx, private_key, proxy):
    async with semaphore:
        user_agent = UserAgent(browsers='chrome', os='macos', platforms='pc').random
        linea = Linea(idx, private_key, user_agent, proxy)
        await asyncio.sleep(random.randint(RandomLeft, RandomRight))
        try:
            if int(mission_type) == 1:
                await linea.clutch_quest()
            elif int(mission_type) == 2:
                await linea.mint_wizards_quest()
            elif int(mission_type) == 3:
                await linea.mint_efrogs_quest()
            elif int(mission_type) == 4:
                await linea.mint_linus_egg_quest()
            elif int(mission_type) == 5:
                await linea.mint_yooldo_quest()
            elif int(mission_type) == 6:
                await linea.mint_frog_wars_quest()
            elif int(mission_type) == 7:
                await linea.mint_acg_quest()
            elif int(mission_type) == 8:
                await linea.mint_toad_quest()
            elif int(mission_type) == 9:
                await linea.mint_ascend_the_end_quest()
            elif int(mission_type) == 10:
                await linea.mint_sending_me_quest()
            elif int(mission_type) == 11:
                await linea.mint_town_story_quest()
            elif int(mission_type) == 12:
                await linea.mint_danielle_quest()
            elif int(mission_type) == 13:
                await linea.mint_demmortal_treasure_quest()
            elif int(mission_type) == 14:
                await linea.mint_foxy_quest()
            elif int(mission_type) == 15:
                await linea.coop_records_quest()
        except Exception as e:
            logger.error(f"account ({linea.idx}) complete quest failed ❌ {e}")


def read_files():
    with open('files/accounts.txt', 'r', encoding='utf-8') as file:
        private_keys = file.read().splitlines()
        private_keys = [k.strip() for k in private_keys]
    with open('files/proxies.txt', 'r', encoding='utf-8') as file:
        proxies = file.read().splitlines()
        proxies = [p.strip() for p in proxies]

    return private_keys, proxies


async def main(sync_num, mission_type):
    private_keys, proxies = read_files()

    semaphore = asyncio.Semaphore(sync_num)
    missions = []

    for idx in range(len(private_keys)):
        private_key = private_keys[idx]
        proxy = proxies[idx]

        missions.append(
            asyncio.create_task(
                start_linea_l3_quest(semaphore, mission_type, idx + 1, private_key, proxy)))

    await asyncio.gather(*missions)


if __name__ == '__main__':
    SyncNum = 3
    RandomLeft = 10
    RandomRight = 20
    MissionType = input(
        """
        请输入任务: 
        1:W1:Crazy Gang
        2:W1:Wizards of Linea
        3:W1:eFrogs
        4:W2:Linus
        5:W2:Yooldo
        6:W2:Frog Wars
        7:W2:ACG
        8:W2:Toad The Great
        9:W3:AscendTheEnd
        10:W3:SendingMe
        11:W3:TownStory
        12:W3:DanielleZosavac
        13:W3:Demmortal Treasure
        14:W3:Foxy
        15:W4:Coop Records
        >>"""
    )
    asyncio.run(main(SyncNum, MissionType))
