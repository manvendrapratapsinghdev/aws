# 📰 NewsRoom

A modeThe application displays news articles with:
- News images (with fallback for missing images)
- Article titles and full descriptions
- Publication dates in readable format
- Article summaries highlighted separately
- Source information
- Verification status with color-coded badges
- Strategic advertisement placements
- Clean pagination controls
- Responsive card layoutnsive news reader application built with Streamlit and Material Design principles. This application fetches news data from an API and displays it in a clean, paginated list format.

## Features

- 🎨 **Material Design UI** - Clean, modern interface following Google's Material Design guidelines
- 📱 **Responsive Design** - Works seamlessly on desktop, tablet, and mobile devices
- 📄 **Pagination** - Efficient browsing with 9 items per page in a 3x3 grid layout
- 🖼️ **Image Handling** - Automatic fallback for missing images
- ⚡ **Performance** - Cached API calls for faster loading
- 🔄 **Error Handling** - Graceful error handling and loading states
- 📅 **Full Article Display** - Shows complete article text with publication dates
- 📝 **Rich Content** - Displays both summary and full description for each article
- ✅ **Verification Status** - Shows article verification status with color-coded badges
- 🖱️ **Interactive Articles** - Click the "Read Full Article" button to view detailed content
- 📱 **3-Column Grid** - Beautiful responsive grid layout (3 columns on desktop, 2 on tablet, 1 on mobile)
- 📢 **Integrated Advertisements** - Strategic ad placements between content for monetization

## Screenshot

The application displays news articles with:
- News images (with fallback for missing images)
- Article titles and full descriptions
- Publication dates in readable format
- Article summaries highlighted separately
- Source information
- Verification status with color-coded badges and icons
- Clean pagination controls
- Responsive card layout

## Installation

1. **Clone or download this project**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```

2. **Open your browser** and navigate to `http://localhost:8501`

3. **Browse the news** using the pagination controls

4. **Click the "📖 Read Full Article" button** at the bottom of any card to view the detailed article

5. **Use the back button** to return to the news list

## API Data Sources

The application fetches data from two endpoints:

1. **News List**: `https://api.npoint.io/0d6177f4e45b79e30b52`
2. **Article Details**: `https://api.npoint.io/d94fa493a4bcd7394480`

Expected data format:
```json
[
  {
    "id": "unique_id",
    "title": "Article Title",
    "short_description": "Article description...",
    "image": "https://example.com/image.jpg"
  }
]
```

## Project Structure

```
NewsRoom/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── .github/
    └── copilot-instructions.md  # Copilot instructions
```

## Technical Details

### Material Design Elements
- **Typography**: Roboto font family
- **Colors**: Material Design color palette with primary blues
- **Shadows**: Elevation-based shadows for depth
- **Animations**: Smooth hover transitions and loading states
- **Cards**: Elevated cards with rounded corners

### Performance Optimizations
- **Caching**: API responses cached for 5 minutes using `@st.cache_data`
- **Lazy Loading**: Only loads items for the current page
- **Efficient Rendering**: Optimized HTML/CSS for fast rendering

### Responsive Design
- **Mobile-first**: Adapts to different screen sizes
- **Flexible Layout**: Cards stack vertically on mobile devices
- **Touch-friendly**: Appropriate button sizes for mobile interaction

## Customization

### Changing Items Per Page
Modify the `ITEMS_PER_PAGE` constant in `app.py`:
```python
ITEMS_PER_PAGE = 9  # Change to your desired number (9 recommended for 3x3 grid)
```

### Styling Customization
The CSS is embedded in the `load_css()` function. You can modify:
- Colors in the gradient backgrounds
- Card sizing and spacing
- Typography and font weights
- Animation timing and effects

### API Endpoint
To use a different API endpoint, update the URL in the `fetch_news_data()` function:
```python
response = requests.get("YOUR_API_ENDPOINT_HERE", timeout=10)
```

## Dependencies

- **streamlit** (>=1.28.0): Web application framework
- **requests** (>=2.31.0): HTTP library for API calls

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Troubleshooting

### Common Issues

1. **API not loading**: Check your internet connection and ensure the API endpoint is accessible
2. **Styling issues**: Clear your browser cache and refresh the page
3. **Performance issues**: The app uses caching - if you need fresh data, wait 5 minutes or restart the app

### Getting Help

If you encounter issues:
1. Check the terminal for error messages
2. Ensure all dependencies are installed correctly
3. Verify the API endpoint is accessible
4. Check your Python version (3.7+ recommended)

---

Built with ❤️ using Streamlit and Material Design principles.
