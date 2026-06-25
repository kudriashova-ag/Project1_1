from django.core.management.base import BaseCommand
from store.models import (
    Category, Product, Attribute, AttributeValue,
    ProductAttribute, Tag, ProductTag
)
from django.utils import timezone
from decimal import Decimal

class Command(BaseCommand):
    help = "Заповнює базу даних тестовими даними"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # ── Очищення ──────────────────────────────────
        self.stdout.write("🧹 Очищення старих даних...")
        ProductTag.objects.all().delete()
        ProductAttribute.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        AttributeValue.objects.all().delete()
        Attribute.objects.all().delete()
        Tag.objects.all().delete()

        # ── Теги ──────────────────────────────────────
        self.stdout.write("🏷️  Створення тегів...")
        tags = {
            slug: Tag.objects.create(name=name, slug=slug)
            for slug, name in [
                ("new",        "Новинка"),
                ("sale",       "Розпродаж"),
                ("bestseller", "Хіт продажу"),
                ("eco",        "Еко"),
                ("premium",    "Преміум"),
            ]
        }

        # ── Атрибути та їх значення ───────────────────
        self.stdout.write("🔧 Створення атрибутів...")

        def make_attr(name, slug, values):
            attr = Attribute.objects.create(name=name, slug=slug)
            return {v: AttributeValue.objects.create(attribute=attr, value=v) for v in values}

        av_color    = make_attr("Колір",    "color",    ["Чорний", "Білий", "Синій", "Червоний", "Зелений"])
        av_size     = make_attr("Розмір",   "size",     ["XS", "S", "M", "L", "XL"])
        av_brand    = make_attr("Бренд",    "brand",    ["Nike", "Adidas", "Puma", "Reebok", "NewBalance"])
        av_material = make_attr("Матеріал", "material", ["Бавовна", "Поліестер", "Шкіра", "Нейлон", "Льон"])

        # ── Хелпери ───────────────────────────────────
        def create_product(name, slug, category, price, sale_price=None, stock=10):
            return Product.objects.create(
                name=name, slug=slug, category=category,
                price=Decimal(str(price)),
                sale_price=Decimal(str(sale_price)) if sale_price else None,
                stock=stock, is_available=True,
                description=f"Опис товару: {name}",
                created_at=now, updated_at=now,
            )

        def add_attrs(product, *attr_values):
            for av in attr_values:
                ProductAttribute.objects.create(product=product, attribute_value=av)

        def add_tags(product, *slugs):
            for slug in slugs:
                ProductTag.objects.create(product=product, tag=tags[slug], tagged_at=now)

        # ── Категорія 1: Футболки ─────────────────────
        self.stdout.write("👕 Категорія: Футболки")
        cat = Category.objects.create(name="Футболки", slug="tshirts")

        p = create_product("Футболка Classic White", "tshirt-classic-white", cat, 299, stock=50)
        add_attrs(p, av_color["Білий"], av_size["M"], av_brand["Nike"], av_material["Бавовна"])
        add_tags(p, "new", "bestseller")

        p = create_product("Футболка Sport Black", "tshirt-sport-black", cat, 399, stock=30)
        add_attrs(p, av_color["Чорний"], av_size["L"], av_brand["Adidas"], av_material["Поліестер"])
        add_tags(p, "bestseller", "sale")

        p = create_product("Футболка Eco Green", "tshirt-eco-green", cat, 449, stock=20)
        add_attrs(p, av_color["Зелений"], av_size["S"], av_brand["Puma"], av_material["Льон"])
        add_tags(p, "eco", "new")

        p = create_product("Футболка Premium Blue", "tshirt-premium-blue", cat, 799, stock=15)
        add_attrs(p, av_color["Синій"], av_size["XL"], av_brand["NewBalance"], av_material["Бавовна"])
        add_tags(p, "premium")

        p = create_product("Футболка Basic Red", "tshirt-basic-red", cat, 199, sale_price=149, stock=100)
        add_attrs(p, av_color["Червоний"], av_size["XS"], av_brand["Reebok"], av_material["Поліестер"])
        add_tags(p, "sale")

        # ── Категорія 2: Кросівки ─────────────────────
        self.stdout.write("👟 Категорія: Кросівки")
        cat = Category.objects.create(name="Кросівки", slug="sneakers")

        p = create_product("Кросівки Air Max White", "sneakers-air-max-white", cat, 2999, stock=25)
        add_attrs(p, av_color["Білий"], av_size["L"], av_brand["Nike"], av_material["Нейлон"])
        add_tags(p, "new", "premium")

        p = create_product("Кросівки Ultraboost Black", "sneakers-ultraboost-black", cat, 3499, stock=10)
        add_attrs(p, av_color["Чорний"], av_size["M"], av_brand["Adidas"], av_material["Поліестер"])
        add_tags(p, "bestseller", "premium")

        p = create_product("Кросівки Eco Run Green", "sneakers-eco-run-green", cat, 1899, sale_price=1599, stock=35)
        add_attrs(p, av_color["Зелений"], av_size["S"], av_brand["Puma"], av_material["Льон"])
        add_tags(p, "eco", "sale")

        p = create_product("Кросівки Classic Blue", "sneakers-classic-blue", cat, 1499, stock=40)
        add_attrs(p, av_color["Синій"], av_size["XL"], av_brand["Reebok"], av_material["Нейлон"])
        add_tags(p, "new")

        p = create_product("Кросівки Red Runner", "sneakers-red-runner", cat, 2199, sale_price=1899, stock=18)
        add_attrs(p, av_color["Червоний"], av_size["XS"], av_brand["NewBalance"], av_material["Шкіра"])
        add_tags(p, "sale", "bestseller")

        # ── Категорія 3: Аксесуари ────────────────────
        self.stdout.write("🎒 Категорія: Аксесуари")
        cat = Category.objects.create(name="Аксесуари", slug="accessories")

        p = create_product("Рюкзак Premium Black", "bag-premium-black", cat, 1299, stock=20)
        add_attrs(p, av_color["Чорний"], av_brand["Nike"], av_material["Нейлон"])
        add_tags(p, "premium", "new")

        p = create_product("Кепка Classic White", "cap-classic-white", cat, 349, stock=60)
        add_attrs(p, av_color["Білий"], av_size["M"], av_brand["Adidas"], av_material["Бавовна"])
        add_tags(p, "bestseller")

        p = create_product("Шкарпетки Eco Pack", "socks-eco-pack", cat, 199, sale_price=149, stock=200)
        add_attrs(p, av_color["Зелений"], av_size["S"], av_brand["Puma"], av_material["Бавовна"])
        add_tags(p, "eco", "sale")

        p = create_product("Пояс Leather Blue", "belt-leather-blue", cat, 599, stock=30)
        add_attrs(p, av_color["Синій"], av_brand["Reebok"], av_material["Шкіра"])
        add_tags(p, "premium")

        p = create_product("Гаманець Red Classic", "wallet-red-classic", cat, 449, sale_price=349, stock=45)
        add_attrs(p, av_color["Червоний"], av_brand["NewBalance"], av_material["Шкіра"])
        add_tags(p, "sale", "new")

        # ── Підсумок ──────────────────────────────────
        self.stdout.write(self.style.SUCCESS("\n✅ Seed завершено!"))
        self.stdout.write(f"   Категорій:  {Category.objects.count()}")
        self.stdout.write(f"   Товарів:    {Product.objects.count()}")
        self.stdout.write(f"   Тегів:      {Tag.objects.count()}")
        self.stdout.write(f"   Атрибутів:  {Attribute.objects.count()}")
        self.stdout.write(f"   Зв'язків:   {ProductAttribute.objects.count()}")