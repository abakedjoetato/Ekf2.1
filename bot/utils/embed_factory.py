
"""
Emerald's Killfeed - Embed Factory
Creates consistent, themed embeds with proper thumbnail placement and no emojis
"""

import logging
import discord
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from pathlib import Path

logger = logging.getLogger(__name__)

class EmbedFactory:
    """
    Factory for creating themed embeds with consistent styling
    - All embeds use proper logo thumbnails on the right side
    - No emojis are used in any embeds
    - Consistent color theming
    - File attachments for assets
    """
    
    # Theme colors
    COLORS = {
        'connection': 0x00d38a,  # Green for connections
        'killfeed': 0xff6b6b,   # Red for killfeed
        'mission': 0x4ecdc4,    # Teal for missions
        'airdrop': 0xffd93d,    # Gold for airdrops
        'helicrash': 0xff8c42,  # Orange for helicrash
        'trader': 0x6c5ce7,     # Purple for trader
        'vehicle': 0x74b9ff,    # Blue for vehicles
        'bounty': 0xe84393,     # Pink for bounties
        'economy': 0x00b894,    # Green for economy
        'leaderboard': 0x0984e3, # Blue for leaderboard
        'error': 0xe74c3c,      # Red for errors
        'success': 0x27ae60,    # Green for success
        'warning': 0xf39c12,    # Orange for warnings
        'info': 0x3498db        # Blue for info
    }
    
    # Asset paths
    ASSETS_PATH = Path('./assets')
    
    # Asset mappings
    ASSETS = {
        'connection': 'Connections.png',
        'killfeed': 'Killfeed.png',
        'mission': 'Mission.png',
        'airdrop': 'Airdrop.png',
        'helicrash': 'Helicrash.png',
        'trader': 'Trader.png',
        'vehicle': 'Vehicle.png',
        'bounty': 'Bounty.png',
        'economy': 'Gamble.png',
        'leaderboard': 'Leaderboard.png',
        'faction': 'Faction.png',
        'weapon': 'WeaponStats.png',
        'suicide': 'Suicide.png',
        'falling': 'Falling.png',
        'main': 'main.png'
    }

    @classmethod
    async def build(cls, embed_type: str, data: Dict[str, Any]) -> Tuple[discord.Embed, Optional[discord.File]]:
        """
        Build a complete embed with proper thumbnail and file attachment
        Returns tuple of (embed, file_attachment)
        """
        try:
            # Get asset info
            asset_filename = cls.ASSETS.get(embed_type, 'main.png')
            asset_path = cls.ASSETS_PATH / asset_filename
            
            # Create file attachment if asset exists
            file_attachment = None
            thumbnail_url = None
            
            if asset_path.exists():
                file_attachment = discord.File(str(asset_path), filename=asset_filename)
                thumbnail_url = f"attachment://{asset_filename}"
            
            # Create base embed
            color = cls.COLORS.get(embed_type, cls.COLORS['info'])
            embed = discord.Embed(
                title=data.get('title', 'Emerald Killfeed'),
                description=data.get('description', ''),
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Set thumbnail on the right side
            if thumbnail_url:
                embed.set_thumbnail(url=thumbnail_url)
            
            # Add fields based on embed type
            if embed_type == 'connection':
                cls._add_connection_fields(embed, data)
            elif embed_type == 'mission':
                cls._add_mission_fields(embed, data)
            elif embed_type == 'killfeed':
                cls._add_killfeed_fields(embed, data)
            elif embed_type == 'suicide':
                cls._add_suicide_fields(embed, data)
            elif embed_type == 'fall':
                cls._add_fall_fields(embed, data)
            elif embed_type == 'airdrop':
                cls._add_airdrop_fields(embed, data)
            elif embed_type == 'helicrash':
                cls._add_helicrash_fields(embed, data)
            elif embed_type == 'trader':
                cls._add_trader_fields(embed, data)
            elif embed_type == 'vehicle':
                cls._add_vehicle_fields(embed, data)
            elif embed_type == 'bounty':
                cls._add_bounty_fields(embed, data)
            elif embed_type == 'economy':
                cls._add_economy_fields(embed, data)
            elif embed_type == 'leaderboard':
                cls._add_leaderboard_fields(embed, data)
            
            # Set footer
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            
            return embed, file_attachment
            
        except Exception as e:
            logger.error(f"Failed to build embed: {e}")
            # Return basic embed as fallback
            fallback_embed = discord.Embed(
                title="System Message",
                description="An error occurred while creating this embed",
                color=cls.COLORS['error'],
                timestamp=datetime.now(timezone.utc)
            )
            fallback_embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return fallback_embed, None

    @classmethod
    def _add_connection_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for connection embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        platform = data.get('platform', 'Unknown')
        server_name = data.get('server_name', 'Unknown Server')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Platform", value=platform, inline=True)
        embed.add_field(name="Server", value=server_name, inline=True)

    @classmethod
    def _add_mission_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for mission embeds"""
        mission_id = data.get('mission_id', '')
        level = data.get('level', 1)
        state = data.get('state', 'UNKNOWN')
        respawn_time = data.get('respawn_time')
        
        # Normalize mission name
        mission_name = cls.normalize_mission_name(mission_id)
        
        embed.add_field(name="Mission", value=mission_name, inline=False)
        embed.add_field(name="Difficulty Level", value=f"Level {level}", inline=True)
        embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)
        
        if respawn_time:
            embed.add_field(name="Respawn Time", value=f"{respawn_time} seconds", inline=True)

    @classmethod
    def _add_killfeed_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for killfeed embeds"""
        killer = data.get('killer_name', data.get('killer', 'Unknown'))
        victim = data.get('victim_name', data.get('victim', 'Unknown'))
        weapon = data.get('weapon', 'Unknown')
        distance = data.get('distance', '0')
        
        # Convert distance to string for comparison
        distance_str = str(distance)
        
        embed.add_field(name="Killer", value=killer, inline=True)
        embed.add_field(name="Victim", value=victim, inline=True)
        embed.add_field(name="Weapon", value=weapon, inline=True)
        
        # Safe distance comparison - convert to float for numeric check
        try:
            distance_num = float(distance_str)
            if distance_num > 0:
                embed.add_field(name="Distance", value=f"{distance_str}m", inline=True)
        except (ValueError, TypeError):
            pass

    @classmethod
    def _add_suicide_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for suicide embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        cause = data.get('cause', 'Suicide')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Cause", value=cause, inline=True)

    @classmethod
    def _add_fall_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for fall death embeds"""
        player_name = data.get('player_name', 'Unknown Player')
        
        embed.add_field(name="Player", value=player_name, inline=True)
        embed.add_field(name="Cause", value="Falling Damage", inline=True)

    @classmethod
    def _add_airdrop_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for airdrop embeds"""
        location = data.get('location', 'Unknown Location')
        state = data.get('state', 'incoming')
        
        embed.add_field(name="Location", value=location, inline=True)
        embed.add_field(name="Status", value=state.title(), inline=True)

    @classmethod
    def _add_helicrash_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for helicrash embeds"""
        location = data.get('location', 'Unknown Location')
        
        embed.add_field(name="Crash Site", value=location, inline=True)
        embed.add_field(name="Status", value="Crashed", inline=True)

    @classmethod
    def _add_trader_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for trader embeds"""
        location = data.get('location', 'Unknown Location')
        
        embed.add_field(name="Location", value=location, inline=True)
        embed.add_field(name="Status", value="Available", inline=True)

    @classmethod
    def _add_vehicle_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for vehicle embeds"""
        vehicle_type = data.get('vehicle_type', 'Unknown Vehicle')
        action = data.get('action', 'spawned')
        
        embed.add_field(name="Vehicle", value=vehicle_type, inline=True)
        embed.add_field(name="Action", value=action.title(), inline=True)

    @classmethod
    def _add_bounty_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for bounty embeds"""
        target = data.get('target', 'Unknown')
        amount = data.get('amount', 0)
        poster = data.get('poster', 'Unknown')
        
        embed.add_field(name="Target", value=target, inline=True)
        embed.add_field(name="Bounty", value=f"{amount:,}", inline=True)
        embed.add_field(name="Posted By", value=poster, inline=True)

    @classmethod
    def _add_economy_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for economy embeds"""
        amount = data.get('amount', 0)
        balance = data.get('balance', 0)
        currency = data.get('currency', 'Emeralds')
        
        embed.add_field(name="Amount", value=f"{amount:,} {currency}", inline=True)
        embed.add_field(name="New Balance", value=f"{balance:,} {currency}", inline=True)

    @classmethod
    def _add_leaderboard_fields(cls, embed: discord.Embed, data: Dict[str, Any]):
        """Add fields for leaderboard embeds"""
        server_name = data.get('server_name', 'Unknown Server')
        stat_type = data.get('stat_type', 'kills')
        
        embed.add_field(name="Server", value=server_name, inline=True)
        embed.add_field(name="Ranking By", value=stat_type.title(), inline=True)

    @classmethod
    def create_mission_embed(cls, title: str, description: str, mission_id: str, 
                           level: int, state: str, respawn_time: Optional[int] = None) -> discord.Embed:
        """Create a mission embed with proper formatting"""
        try:
            # Get mission color based on level
            if level >= 5:
                color = 0xff0000  # Red for highest level
            elif level >= 4:
                color = 0xff8c00  # Orange for high level
            elif level >= 3:
                color = 0xffd700  # Gold for medium level
            else:
                color = cls.COLORS['mission']  # Default teal for low level
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now(timezone.utc)
            )
            
            # Add mission details
            mission_name = cls.normalize_mission_name(mission_id)
            embed.add_field(name="Mission", value=mission_name, inline=False)
            embed.add_field(name="Difficulty Level", value=f"Level {level}", inline=True)
            embed.add_field(name="Status", value=state.replace('_', ' ').title(), inline=True)
            
            if respawn_time:
                embed.add_field(name="Respawn Time", value=f"{respawn_time} seconds", inline=True)
            
            # Set thumbnail for mission
            asset_path = cls.ASSETS_PATH / cls.ASSETS['mission']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['mission']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create mission embed: {e}")
            return cls._create_fallback_embed("Mission Update", "Mission status has changed")

    @classmethod
    def create_airdrop_embed(cls, state: str, location: str, timestamp: datetime) -> discord.Embed:
        """Create an airdrop embed"""
        try:
            embed = discord.Embed(
                title="Airdrop Incoming",
                description="Supply drop detected on radar",
                color=cls.COLORS['airdrop'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Status", value=state.title(), inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['airdrop']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['airdrop']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create airdrop embed: {e}")
            return cls._create_fallback_embed("Airdrop", "Supply drop detected")

    @classmethod
    def create_helicrash_embed(cls, location: str, timestamp: datetime) -> discord.Embed:
        """Create a helicrash embed"""
        try:
            embed = discord.Embed(
                title="Helicopter Crash",
                description="Aircraft down, investigate for valuable loot",
                color=cls.COLORS['helicrash'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Crash Site", value=location, inline=True)
            embed.add_field(name="Status", value="Crashed", inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['helicrash']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['helicrash']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create helicrash embed: {e}")
            return cls._create_fallback_embed("Helicrash", "Helicopter crashed")

    @classmethod
    def create_trader_embed(cls, location: str, timestamp: datetime) -> discord.Embed:
        """Create a trader embed"""
        try:
            embed = discord.Embed(
                title="Trader Arrival",
                description="Black market dealer has arrived",
                color=cls.COLORS['trader'],
                timestamp=timestamp
            )
            
            embed.add_field(name="Location", value=location, inline=True)
            embed.add_field(name="Status", value="Available", inline=True)
            
            # Set thumbnail
            asset_path = cls.ASSETS_PATH / cls.ASSETS['trader']
            if asset_path.exists():
                embed.set_thumbnail(url=f"attachment://{cls.ASSETS['trader']}")
            
            embed.set_footer(text="Powered by Discord.gg/EmeraldServers")
            return embed
            
        except Exception as e:
            logger.error(f"Failed to create trader embed: {e}")
            return cls._create_fallback_embed("Trader", "Trader has arrived")

    @classmethod
    def _create_fallback_embed(cls, title: str, description: str) -> discord.Embed:
        """Create a basic fallback embed"""
        return discord.Embed(
            title=title,
            description=description,
            color=cls.COLORS['info'],
            timestamp=datetime.now(timezone.utc)
        )

    @classmethod
    def normalize_mission_name(cls, mission_id: str) -> str:
        """Convert mission ID to readable name"""
        mission_mappings = {
            'GA_Airport_mis_01_SFPSACMission': 'Airport Mission #1',
            'GA_Airport_mis_02_SFPSACMission': 'Airport Mission #2',
            'GA_Airport_mis_03_SFPSACMission': 'Airport Mission #3',
            'GA_Airport_mis_04_SFPSACMission': 'Airport Mission #4',
            'GA_Military_02_Mis1': 'Military Base Mission #2',
            'GA_Military_03_Mis_01': 'Military Base Mission #3',
            'GA_Military_04_Mis1': 'Military Base Mission #4',
            'GA_Beregovoy_Mis1': 'Beregovoy Settlement Mission',
            'GA_Settle_05_ChernyLog_Mis1': 'Cherny Log Settlement Mission',
            'GA_Ind_01_m1': 'Industrial Zone Mission #1',
            'GA_Ind_02_Mis_1': 'Industrial Zone Mission #2',
            'GA_KhimMash_Mis_01': 'Chemical Plant Mission #1',
            'GA_KhimMash_Mis_02': 'Chemical Plant Mission #2',
            'GA_Bunker_01_Mis1': 'Underground Bunker Mission',
            'GA_Sawmill_01_Mis1': 'Sawmill Mission #1',
            'GA_Settle_09_Mis_1': 'Settlement Mission #9',
            'GA_Military_04_Mis_2': 'Military Base Mission #4B',
            'GA_PromZone_6_Mis_1': 'Industrial Zone Mission #6',
            'GA_PromZone_Mis_01': 'Industrial Zone Mission A',
            'GA_PromZone_Mis_02': 'Industrial Zone Mission B',
            'GA_Kamensk_Ind_3_Mis_1': 'Kamensk Industrial Mission',
            'GA_Kamensk_Mis_1': 'Kamensk City Mission #1',
            'GA_Kamensk_Mis_2': 'Kamensk City Mission #2',
            'GA_Kamensk_Mis_3': 'Kamensk City Mission #3',
            'GA_Krasnoe_Mis_1': 'Krasnoe City Mission',
            'GA_Vostok_Mis_1': 'Vostok City Mission',
            'GA_Lighthouse_02_Mis1': 'Lighthouse Mission #2',
            'GA_Elevator_Mis_1': 'Elevator Complex Mission #1',
            'GA_Elevator_Mis_2': 'Elevator Complex Mission #2',
            'GA_Sawmill_02_1_Mis1': 'Sawmill Mission #2A',
            'GA_Sawmill_03_Mis_01': 'Sawmill Mission #3',
            'GA_Bochki_Mis_1': 'Barrel Storage Mission',
            'GA_Dubovoe_0_Mis_1': 'Dubovoe Resource Mission',
        }
        
        return mission_mappings.get(mission_id, mission_id.replace('_', ' ').title())

    @classmethod
    def get_mission_level(cls, mission_id: str) -> int:
        """Determine mission difficulty level"""
        # High-tier missions (level 5)
        high_tier = [
            'GA_Airport_mis_04_SFPSACMission',
            'GA_Military_04_Mis1',
            'GA_Military_04_Mis_2',
            'GA_Bunker_01_Mis1',
            'GA_KhimMash_Mis_02'
        ]
        
        # Medium-high tier missions (level 4)
        medium_high_tier = [
            'GA_Airport_mis_03_SFPSACMission',
            'GA_Military_03_Mis_01',
            'GA_KhimMash_Mis_01',
            'GA_Kamensk_Mis_3',
            'GA_Elevator_Mis_2'
        ]
        
        # Medium tier missions (level 3)
        medium_tier = [
            'GA_Airport_mis_02_SFPSACMission',
            'GA_Military_02_Mis1',
            'GA_Ind_02_Mis_1',
            'GA_Kamensk_Mis_1',
            'GA_Kamensk_Mis_2',
            'GA_Krasnoe_Mis_1',
            'GA_Vostok_Mis_1',
            'GA_Elevator_Mis_1',
            'GA_Sawmill_03_Mis_01'
        ]
        
        if mission_id in high_tier:
            return 5
        elif mission_id in medium_high_tier:
            return 4
        elif mission_id in medium_tier:
            return 3
        else:
            return 2  # Low tier missions
