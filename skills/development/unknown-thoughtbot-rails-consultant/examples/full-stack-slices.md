# Break apart your features into full-stack slices

I often see people split work into horizontal slices. Ticket A: database tables
and models. Ticket B: controllers. Ticket C: front-end.

There's something better &mdash; split the work into full-stack slices.

## The full-stack slice

Think of your feature like a stack of pancakes, where each pancake represents a
layer of your system. Eat a piece of all pancakes at the same time. Don't eat
them one at a time.

![Two images. Left has three pancakes on a plate with an arrow cutting through all three. Right image has three separate pancakes flat on the plate with red X across them.](https://images.thoughtbot.com/blog-vellum-image-uploads/kPlHvn2ASAexM5od3NIY_pancakes-stack-flat.png)

That may seem unrealistic. After all, there's usually logic that is shared by
every part of the feature.

Sometimes features are more like icebergs, where a small change in one layer
corresponds to a large change in a separate layer. For example, the UI may have
a smaller footprint than the back-end. That's okay. Handle more of the back-end
in a ticket, but cut vertically through the iceberg. Don't cut horizontally.

![Two images. Left has iceberg with a green line cutting vertically through it. It takes a little off the top but a lot off the bottom. Right image is an iceberg with a horizontal crack through it. A red X is overlaid.](https://images.thoughtbot.com/blog-vellum-image-uploads/dYj0u4mWRYWFt870ZjV3_icerberg-vertical-horizontal.png)

## Why it's better

- Work iteratively. In the [post agile] world, everybody pretends to work in
  iterations. But can we ship at the end of our iteration? If we build the
  database and tables in one iteration, our customers don't receive any new
  work. But if we ship a sliver of the full stack, they get something.

- Discover the glue code. When working in front-end and back-end slices, we
  often overlook the code that ties the two slices together. And that spells
  trouble at the eleventh hour &mdash; an incorrect abstraction or a missed
  parameter, and we're having to order pizza for dinner and work into the night.
  But if we build a full-stack slice, we need the glue code while building the
  slice. No surprises Friday night.

- Learn quickly. When working with full-stack slices, we may find a large
  roadblock that forces our project in a new direction. Or we may ship a portion
  of our feature and receive customer feedback that changes our roadmap.

- Stay nimble. We know one thing about the future: it will bring change.
  External forces change the highest priority project today into a low priority
  project tomorrow. If we only work on one layer of our system and priorities
  change, our customers will not get any part of the feature. But if we ship
  full-stack slices, we can change projects at the drop of a hat with minimal
  loss.

- Only write the code you need. When working on the back-end in isolation from
  the final product, we work with incomplete information &mdash; guessing what
  the front-end will need. So, we over-engineer solutions that take longer to
  develop and create unused code paths that we must then maintain.

[post agile]: https://pragdave.me/blog/2014/03/04/time-to-kill-agile.html

## An example

Let's look at an example from a recent project.

I was assigned three tickets that considered the front-end and back-end as two
completely different aspects of the application:

![Front-end and back-end split completely as two different tablets. Front-end has UI. Back-end has some plumbing and a database.](https://images.thoughtbot.com/blog-vellum-image-uploads/aMCVIrOTaGjOih1PO28O_split-into-frontend-backend.png)

- Ticket X: build the back-end &mdash; controllers, models, all the
  functionality needed for rendering, filtering, and searching.

- Ticket Y: build the front end &mdash; navigation, UI cards, a sidebar for
  filtering, and a navbar for search and a create button.

- Ticket Z: build a sliding panel of the UI that reused a lot of back-end work.

Tickets X and Y were completely separated into front-end and back-end. The
complexity of each was high, meaning I could spend a lot of time building things
I assumed the other ticket would need.

Ticket Z was separate from the other two, and it was mostly front-end work since
it used existing back-end functionality.

### Looking from the perspective of the user

Instead of following those tickets, I looked at the UI from the perspective of
the user to find pieces that could be shipped separately. That gave me four
major sections with some subsections: A.1, A.2, B, C.1, C.3, and D.

![The UI broken down into four sections: A, B, C, D. A is the UI card itself. B is a sidebar on the left of the main section. C is the action buttons on the top right nav. D is a transparent sliding panel.](https://images.thoughtbot.com/blog-vellum-image-uploads/MVs5PFeTRVa78lTMqlmA_split-into-full-stack-sections.png)

- **A.1**: Display the list of items. This was the first slice of the iceberg,
  so I included a lot of the shared logic: navigation (a user has to get to the
  page), the UI cards with essential information, and all the back-end work
  needed to render them.

- **A.2**: Each card in the list had some complex interactive elements. I
  separated those into a new ticket. It mostly included UI work and small
  back-end pieces.

- **B**: Filtering in the sidebar so that users could narrow down the cards they
  see. This was blocked by A.1.

- **C.1**: Adding search that would filter the cards to the ones matching the
  query. Much like B, this one needed the core of A.1.

- **C.2**: Creating a new item. Most of the back-end logic for this already
  existed. So this was a trivial UI addition.

- **D**: Adding the sliding panel. In a new application, I would have made the
  sliding panel its own feature made of full-stack slices. Thankfully, most of
  the back-end was already built. So this was primarily UI work.

You can decide where to put the first slice of the iceberg that has shared
logic. I put it in A.1 because it seemed like the most important part of the
feature. Without it, users would not get any value from the rest.

Some of the other work &mdash; like B, C.1, and C.2 &mdash; became thin slivers
of full-stack work. And that made for concise pull requests. Avoid the
temptation to group those thin slivers with something else. I have seen many
"simple" ancillary tasks unearth complex issues and delay the release of the
core feature.

## Full stack depends on your stack

You may think these lessons don't apply to you because you build APIs or
single-page applications. But it does. Full-stack is whatever your fullest stack
can be.

If you build APIs, the consumers of the API are your users. And they will
benefit from an endpoint that returns a list of items even before you allow them
to search or filter those items.

Likewise, if you build single-page applications, splitting your front-end work
into discrete portions that you can deliver separately will bring value to your
users faster while keeping you nimble.

**Break apart your features into full-stack slices** whatever your stack.
