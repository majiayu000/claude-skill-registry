---
name: add-social-media-header
description: Add professional social media headers to README files and documentation to enhance engagement and visibility across LinkedIn, YouTube, GitHub, and X (Twitter). Use when you need to add or update social media badges with clickable links to your profiles.
---

# Add Social Media Header

Add a professional social media header with styled badges and links to enhance your content's visibility and engagement.

## How to use

When asked to add a social media header to your README or documentation:

1. **Gather your profile information**: Get your YouTube channel ID, GitHub username, LinkedIn URL, and X/Twitter URL
2. **Identify insertion point**: The header should go at the top of your README, right after the main title
3. **Customize the template**: Replace all placeholder values with your actual profile information
4. **Insert into file**: Add the complete block to your README

### Template

```markdown
<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/YOUR_CHANNEL_ID?style=for-the-badge&logo=youtube&logoColor=white&color=red)](YOUR_YOUTUBE_URL) [![GitHub followers](https://img.shields.io/github/followers/YOUR_USERNAME?style=for-the-badge&logo=github&logoColor=white)](YOUR_GITHUB_URL) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin&logoColor=white)](YOUR_LINKEDIN_URL) [![X Follow](https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white)](YOUR_X_URL)

</div>
```

**Important:** Keep all badges on a single line (no line breaks between them) for proper horizontal alignment.

Replace the following placeholders with your actual information:
- `YOUR_CHANNEL_ID` - Your YouTube channel ID (find in YouTube channel settings, usually looks like: UC140iBrEZbOtvxWsJ-Tb0lQ)
- `YOUR_USERNAME` - Your GitHub username (e.g., 0GiS0)
- `YOUR_YOUTUBE_URL` - Full URL to your YouTube channel (e.g., https://www.youtube.com/c/YourChannelName)
- `YOUR_GITHUB_URL` - Full URL to your GitHub profile (e.g., https://github.com/YourUsername)
- `YOUR_LINKEDIN_URL` - Full URL to your LinkedIn profile (e.g., https://www.linkedin.com/in/yourprofile/)
- `YOUR_X_URL` - Full URL to your X/Twitter profile (e.g., https://twitter.com/YourHandle)

## Example with Real URLs

Here's a complete example with actual URLs that you can adapt (all badges on one line):

```markdown
<div align="center">

[![YouTube Channel Subscribers](https://img.shields.io/youtube/channel/subscribers/UC140iBrEZbOtvxWsJ-Tb0lQ?style=for-the-badge&logo=youtube&logoColor=white&color=red)](https://www.youtube.com/c/GiselaTorres?sub_confirmation=1) [![GitHub followers](https://img.shields.io/github/followers/0GiS0?style=for-the-badge&logo=github&logoColor=white)](https://github.com/0GiS0) [![LinkedIn Follow](https://img.shields.io/badge/LinkedIn-Follow-blue?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/giselatorresbuitrago/) [![X Follow](https://img.shields.io/badge/X-Follow-black?style=for-the-badge&logo=x&logoColor=white)](https://twitter.com/0GiS0)

</div>
```

## Important Notes

### Why badges might not render

If you only see the `<div align="center">` and not the badges:

1. **GitHub might not be rendering shields.io badges**: Refresh your browser
2. **Internet connection required**: Badge images are fetched from shields.io, so internet is needed
3. **Network blocked**: Some corporate networks block external image sources

### Troubleshooting

If badges don't appear:
- Verify your YouTube channel ID is correct
- Check that all URLs are complete and valid (start with https://)
- **Ensure all badges are on a single line** (this is important for proper alignment)
- Try accessing the badge URLs directly in your browser:
  - YouTube: `https://img.shields.io/youtube/channel/subscribers/YOUR_CHANNEL_ID?style=for-the-badge&logo=youtube`
- Make sure there are blank lines between the `<div>` tag and the badges line

## Customization options

### Style variations
- `style=for-the-badge` - Modern, rectangular badges (recommended)
- `style=flat` - Flat design
- `style=plastic` - Glossy appearance
- `style=flat-square` - Square badges

### Colors
Add custom colors to badges using the `color=` parameter (hex without #):
- YouTube: `color=FF0000` (red)
- GitHub: `color=000000` (black) or `color=FFFFFF` (white)
- LinkedIn: `color=0077b5` (official LinkedIn blue)
- X: `color=000000` (black)

### Badge text
Update the badge labels (e.g., "Follow", "Subscribe", "Connect") to match your preference.

## Pro Tips

1. **Keep badges on one line**: Don't add line breaks between badges for proper horizontal alignment
2. **Keep it simple**: Don't add more than 4-5 badges to avoid clutter
3. **Test locally**: Use GitHub's markdown preview or VS Code to verify rendering
4. **Update regularly**: If your follower count changes significantly, update the label if needed
