const { chromium } = require('playwright');

(async () => {
  console.log('Launching browser...');
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  console.log('Navigating to Facebook...');
  await page.goto('https://www.facebook.com');

  console.log('Waiting 5 seconds for you to log in if needed...');
  await page.waitForTimeout(5000);

  console.log('Taking screenshot...');
  await page.screenshot({ path: 'facebook_current.png' });

  console.log('Getting page content...');
  const content = await page.content();

  if (content.includes('ALHAMDULILLAH for Everything')) {
    console.log('Found the post! Looking for delete button...');

    // Look for the post and click the menu
    const postText = await page.locator('text=ALHAMDULILLAH for Everything').first();
    if (postText) {
      console.log('Found post text, looking for menu button...');
      // Find the nearest menu button (three dots)
      const menuButton = await page.locator('[aria-label*="Action"]').first();
      await menuButton.click();
      await page.waitForTimeout(1000);

      // Click delete option
      const deleteButton = await page.locator('text=/Delete|Move to trash/i').first();
      await deleteButton.click();
      await page.waitForTimeout(1000);

      // Confirm deletion
      const confirmButton = await page.locator('text=/Delete|Confirm/i').first();
      await confirmButton.click();

      console.log('Post deleted!');
    }
  } else {
    console.log('Post not found. It may not have been published.');
  }

  console.log('Done. Browser will stay open for 10 seconds...');
  await page.waitForTimeout(10000);

  await browser.close();
})();
