A few months ago my colleague [Josh Steiner] wrote a comprehensive post on [How
We Test Rails Applications], detailing the different types tests we write and
the various technologies that go with them. In this follow up, we will take a
closer look at thoughtbot's testing workflow.

We use a process known as "Outside-in testing", driving our development from
high-level tests and working our way down to lower-level concerns. Say we are
working on an e-commerce site and want to implement the following story:

> As a guest, I can add items to my shopping cart so that I can keep on shopping

Before we start thinking about models, controllers, or other architectural
concerns we write a high-level RSpec feature test that describes the behavior from
the user's perspective.

```ruby
# spec/features/guest_adds items_to_shopping_cart_spec.rb
feature 'Guest adds items to shopping cart' do
  scenario 'via search' do
    item = create(:item)

    visit root_path
    fill_in 'Search', with: item.name
    click_on 'Search Catalogue'

    click_on item.name
    click_on 'Add to Cart'
    click_on 'Shopping Cart'

    expect(page).to have_content(item.name)
    expect(page).to have_content("Subtotal: #{item.price}")
  end
end
```

Depending on how much of the application is implemented, this test could break
in multiple places. If this were a newly-generated application we might need to
implement a home page. Once we have a home page we would probably get an error
while attempting to use the search bar saying that 'No such route exists'. This
leads us to implement a `/items` route.

```ruby
# config/routes.rb
# ...
resources :items, only: [:index]
# ...
```

The next few errors walk us through creating an `ItemsController`, with an
empty `index` action and corresponding view. Now that we can successfully click
on "Search Catalogue", we get an error saying that there the desired item does
not appear in the search results so we expose some items in the controller and
display them in the view.

```ruby
# app/controllers/items_controller.rb
#...
def index
  @items = Item.search(params[:search_query])
end
#...
```

```erb
# app/views/items/index.html.erb
<% @items.each do |item| %>
  <%= link_to item.name, item %>
<% end %>
```

This gives us a new error saying that there is no method `search` defined
`Item`. At this point, we drop down a level of abstraction and write a unit
test for `Item`.

```ruby
# spec/models/item_spec.rb
describe Item, '.search' do
  it 'filters items by the search term' do
    desired_item = create(:item)
    other_item = create(:item)

    expect(Item.search(desired_item.name)).to eq [desired_item]
  end
end
```

This test leads us to correctly implement `Item.search`:

```ruby
# app/models/item.rb
#...
def self.search(term)
  where(name: term)
end
#...
```

Now the unit test passes so we go back up to our feature test. We can
successfully click on the item's name in the search results!

We keep following this pattern for the remaining test failures, dropping down
to the unit test level when necessary, until we have a green test suite. Now
our story has been successfuly implemented!

## Mocking and Stubbing

The goal of a feature test is to test the real system from end-to-end from the
user's perspective. To do this, we use real database records and don't mock or
stub any of our objects. We _do_ stub calls to external websites (via webmock
or a fake) since the network can be unreliable. Our tests should run without an
internet connection.

When dropping down to the unit test level, we aggressively mock/stub out
dependencies and collaborators. The goal of a unit test is to prove the
functionality of the object being tested, not the functionality of its
collaborators. Difficulty in testing two objects in isolation from each other
often points to too tight coupling between them.

## Further Reading

For some more great articles on testing, check out:

- [How we Test Rails Applications]
- [Don't Stub the System Under Test]
- [Feature tests with Capybara]

[Josh Steiner]: https://twitter.com/josh_steiner
[How We Test Rails Applications]: https://thoughtbot.com/blog/how-we-test-rails-applications
[Don't Stub the System Under Test]: https://thoughtbot.com/blog/don-t-stub-the-system-under-test
[Feature tests with Capybara]: https://thoughtbot.com/blog/using-capybara-to-test-javascript-that-makes-http
