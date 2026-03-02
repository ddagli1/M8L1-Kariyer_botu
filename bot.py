import discord
from discord.ext import commands
from discord.ui import View, Select
from config import TOKEN, DATABASE
from logic import DB_Manager

# Bot yetkileri ve başlatılması
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Veri tabanı yöneticisini tanımla
db = DB_Manager(DATABASE)

class CareerSelect(Select):
    def __init__(self):
        # Kullanıcının seçebileceği ana kategoriler
        options = [
            discord.SelectOption(label="Teknoloji", description="Yazılım, Veri, Siber Güvenlik", emoji="💻"),
            discord.SelectOption(label="Yaratıcı Sanatlar", description="Tasarım, İçerik Üretimi", emoji="🎨"),
            discord.SelectOption(label="İş Dünyası", description="E-Ticaret, Pazarlama, Yönetim", emoji="📈")
        ]
        super().__init__(placeholder="İlgini çeken bir alan seç...", options=options)

    async def callback(self, interaction: discord.Interaction):
        # Seçilen kategoriye göre veritabanından meslekleri çek
        selected_category = self.values[0]
        careers = db.get_careers_by_category(selected_category)
        
        if not careers:
            await interaction.response.send_message(
                f"**{selected_category}** kategorisinde henüz bir demo verisi bulunmuyor.", 
                ephemeral=True
            )
            return

        # Sonuçları daha güzel göstermek için bir Embed oluşturuyoruz
        embed = discord.Embed(
            title=f"🚀 {selected_category} Alanındaki Kariyer Yolları",
            description=f"Senin için seçtiğimiz en popüler yollar şunlar:",
            color=discord.Color.green()
        )

        for name, desc in careers:
            embed.add_field(name=name, value=desc, inline=False)

        embed.set_footer(text="Geleceğin seni bekliyor! Başka bir kategori seçebilirsin.")
        
        # Sadece seçimi yapan kullanıcının göreceği şekilde yanıt ver (ephemeral=True)
        # Veya herkesin görmesi için bu parametreyi kaldırabilirsin
        await interaction.response.send_message(embed=embed, ephemeral=True)

class CareerBotView(View):
    def __init__(self):
        super().__init__()
        self.add_item(CareerSelect())

@bot.event
async def on_ready():
    # Bot açıldığında veritabanı kontrolü yap (yoksa oluşturur)
    db.create_tables()
    print(f'Bot aktif! Giriş yapıldı: {bot.user}')

@bot.command()
async def basla(ctx):
    """Kullanıcıya karşılama mesajı ve seçim menüsü gönderir"""
    embed = discord.Embed(
        title="Kariyer Danışmanına Hoş Geldin! 👋",
        description=(
            "Yeni bir kariyer yolu keşfetmek için doğru yerdesin.\n\n"
            "Aşağıdaki menüden **ilgi alanını seç**, sana özel önerilerimizi listeyelim!"
        ),
        color=discord.Color.blue()
    )
    # Görsel bir dokunuş:
    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1063/1063376.png")
    
    await ctx.send(embed=embed, view=CareerBotView())

@bot.command()
async def yardim(ctx):
    """Botun nasıl kullanılacağını açıklar"""
    help_text = (
        "**Kariyer Botu Komutları:**\n"
        "`!basla` - Kariyer yolculuğunu başlatır ve menüyü açar.\n"
        "`!yardim` - Bu mesajı gösterir."
    )
    await ctx.send(help_text)

# Botu çalıştır
if __name__ == "__main__":
    bot.run(TOKEN)
