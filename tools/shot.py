import asyncio,sys
from playwright.async_api import async_playwright
URL=sys.argv[1]; OUT='/workspace/distributor-shots/'
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',args=['--no-sandbox'])
        errs=[]
        for name,vp,th in [('desktop',{'width':1360,'height':900},False),('mobile',{'width':390,'height':844},False),('desktop-th',{'width':1360,'height':900},True)]:
            pg=await b.new_page(viewport=vp)
            pg.on('console',lambda m: errs.append((name,m.text)) if m.type=='error' else None)
            pg.on('pageerror',lambda e: errs.append((name,str(e))))
            await pg.goto(URL,wait_until='networkidle')
            if th: await pg.click('#lthBtn'); await pg.wait_for_timeout(400)
            await pg.screenshot(path=OUT+f'{name}-top.png')
            await pg.locator('#match').scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
            await pg.screenshot(path=OUT+f'{name}-match.png')
            if name=='desktop':
                await pg.select_option('#tc','SA'); await pg.locator('#trip').scroll_into_view_if_needed(); await pg.wait_for_timeout(300)
                await pg.screenshot(path=OUT+'desktop-trip.png')
                await pg.fill('input[name=name]','Test Co'); await pg.check('input[name=j]'); await pg.check('input[name=w]'); await pg.click('#addForm button[type=submit]'); await pg.wait_for_timeout(500)
                n=await pg.locator('#mine .card').count(); print('mine cards',n)
                async with pg.expect_download() as dl: await pg.click('#leadCsv')
                d=await dl.value; print('csv',d.suggested_filename)
                await pg.locator('#mine button[data-del]').first.click(); await pg.wait_for_timeout(300)
                print('after delete',await pg.locator('#mine .card').count())
                print('rows',await pg.locator('#leadRows tr').count(),'dist',await pg.locator('#distCards .card').count())
            if name=='mobile':
                sw=await pg.evaluate('document.documentElement.scrollWidth'); print('mobile scrollWidth',sw)
            await pg.close()
        print('errors',errs)
        await b.close()
asyncio.run(main())
