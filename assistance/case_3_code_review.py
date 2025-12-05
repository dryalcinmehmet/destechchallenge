def get_dashboard_stats(request):
    """
    len(AssistanceRequest.objects.all()) ->  Bütün AssistanceRequest kayıtlarını çekmeye çalışır ve bunuda Ram üzerinde yapar.
    Eğer db'de 100k + kayıt var ise ki 10k bile olsa Ram aaşırı yüklenmeye başlar ve sonunda sunucunun kitlenemesine sebebiyet verir.
    Üstelik çekilen kayıtların len() ile countu alınmaya çalışılmış. Yani Python kendi içinde sayıyor. Gereksiz network I/O ve performans
    kaybı.

    Uygun çözüm: Count işini database tarafına bırakmak ve sonucu almak. Bunun içinde len(AssistanceRequest.objects.all()) kodu yerine

    total_count = AssistanceRequest.objects.count() kullanmak lazımdır. Arada ciddi performans ve hız farkı vardır. Bunu rakamsal olarak veremem
    ama profiling yapıp aradaki devasa farkı 10k+ record databasede görebiliriz.

    """
    # 1. Potansiyel Hata
    all_requests = AssistanceRequest.objects.all()
    total_count = len(all_requests)
    active_providers = []

    """
    Burada da benzer şekilde bütün provider objeleri çekilip sonra Python ile filtreleme yapılmaya çalışılmış. Buda kritik bir performans hatasıdır.
    last_ping karşılaştırması her döngüde çalışıyor bariz (n+1) problemi görünmekte. Burada aslında database tarafında bir satır kod ile 
    rahatlıkla çözülebeilecek mesele. Binlerce provider olduğunu düşünürsek pc nin fanı çalışmaya başlayacağından eminim. Tabi şunuda göz önünde
    tutmak lazım örneğin sadece 100 reecord içeren tabloda test yapıldığında sonuçlar arasında ciddi farklar olmayacaktır. Ama data büyüdükçe
    aradaki performans ve response time farkı logaritmik olarak artacaktır. 

    Uygun çözüm: threshold = timezone.now() - timedelta(minutes=5)
                 active_count = Provider.objects.filter(is_active=True, last_ping__gt=threshold).count() 
    
                 Tek SQL sorgusu ile çözülebilir.
    """
    # 2. Potansiyel Hata
    providers = Provider.objects.all()
    for p in providers:
        # Son 5 dakikada ping atmış olanlar
        if p.is_active and p.last_ping > datetime.now() - timedelta(minutes=5):
            active_providers.append(p)

    """
    Log.objects.filter(level='ERROR')[:5] -> Burada şöyle bir sıkıntı var. Bu kod tablodaki ERROR olan rastgele 5 satırı döndürür. Yani buda her 
    seferinde farklı sonuçlar görmemize sebebp olur. Üstelik loglardaki bütün log satırlarını çekiyor. Ve hepsi için ayrı model objesi 
    create ediyor. Sonucunda sadece 'message' gerektiği için çok maliyetli bir yazım tarzı olmuş. Çok daha basitçe flat atılırsa db den artı order_by
    eklenmesi indexleme açısından büyük hız katar. Ve nihayetinde 5 adet model objesini handle etmek yerine 5 adet string handle etmek daha iyi bir seçimdir.

    Uygun çözüm: log_messages= Log.objects.filter(level='ERROR').order_by('-created_at').values_list('message', flat=True)[:5]

    Bu bölümdeki diğer gözüme takılan kısım return objesinin bir serialize edilmiş dictionary olması. Bununla beraber fonksiyon request ile beslenmiş.
    Bu fonksiyon eğer ki - direk response dönecek fonksiyon ise - herhangi bir GET methodu içinde direk return edilmiş olabilir bu durumda DRF için şu
    kod kullanılmalıdır.

    from rest_framework.response import Response

    return Response({
        "total": total_count,
        "active": len(active_providers),
        "logs": log_messages
    }) 

    Eğer sadece json alıp GET methodu içerisinde zaaten Response ediliyorsa o zaman hata var diyemem tabi onu bilmiyoruz.
    """

    # 3. Hata Potansiyeli
    logs = Log.objects.filter(level="ERROR")[:5]
    log_messages = [l.message for l in logs]
    return {"total": total_count, "active": len(active_providers), "logs": log_messages}
