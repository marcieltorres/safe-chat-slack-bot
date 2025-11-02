Jekyll::Hooks.register :site, :post_write do |site|
  sitemap_path = File.join(site.dest, 'sitemap.xml')
  
  if File.exist?(sitemap_path)
    content = File.read(sitemap_path)
    
    # Remove problematic XML namespace attributes
    fixed_content = content.gsub(/ xmlns:xsi="[^"]*" xsi:schemaLocation="[^"]*"/, '')
    
    File.write(sitemap_path, fixed_content)
    Jekyll.logger.info "Sitemap:", "XML namespace attributes removed for better search engine compatibility"
  end
end