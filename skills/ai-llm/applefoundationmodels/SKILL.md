   ---
    name: "AppleFoundationModels"
    description: "Use Apple's on-device **Foundation Models** framework (iOS/iPadOS/macOS 26.0+) for natural language understanding, structured data generation, and tool-assisted tasks in apps."
    version: "1.0"
    dependencies:
      - iOS 26.0 or later (Apple Intelligence enabled)
      - iPadOS 26.0 or later 
      - macOS 26.0 or later 
      - Mac Catalyst 26.0 or later 
      - visionOS 26.0 or later 
    ---

# Instructions

- **On-Device Foundation Model:** Apple's Foundation Models framework
  provides access to a \~3 billion-parameter large language model
  running entirely
  on-device[\[1\]](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/#:~:text=The%20Foundation%20Models%20framework%20is,when%20Apple%20Intelligence%20is%20enabled).
  This model powers **Apple Intelligence** features and runs offline at
  no extra cost, ensuring user data stays
  private[\[2\]](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/#:~:text=With%20the%20release%20of%20iOS,and%20help%20users%20in%20new).
  Always check that the device supports Apple Intelligence and that the
  model is available before use (e.g. via
  `SystemLanguageModel.availability`)[\[3\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=emotions,availability%20property%20on%20the%20SystemLanguageModel).

- **Session and Context:** Interactions with the model occur through a
  stateful `LanguageModelSession`. Creating a session optionally takes
  **developer-provided instructions** (system prompts) to set the
  model's role, style, or other
  guidelines[\[4\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=stateful%20sessions,you%20can%20provide%20custom%20instructions)[\[5\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=instructions%20will%20be%20used%20if,you%20don%E2%80%99t%20specify%20any).
  **Do not** inject untrusted user input into these instructions, since
  the model prioritizes developer instructions over user
  prompts[\[6\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=instructions%20will%20be%20used%20if,you%20don%E2%80%99t%20specify%20any).
  The session maintains a **Transcript** of all turns; multi-turn
  conversations within one session will automatically include context
  from previous prompts and
  responses[\[7\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Now%20that%20you%20have%20initialized,back%20to%20writing%20a%20haiku).
  Avoid concurrent requests on a single session (the model can handle
  only one prompt at a time). Use `session.isResponding` or await the
  response future to ensure the prior request completes before sending
  another[\[8\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=One%20more%20important%20thing%20to,that%20are%20backed%20by%20adapters).

- **Natural Language Understanding (NLU):** The foundation model can
  interpret and extract meaning from text to perform tasks like
  classification, tagging, summarization, or entity extraction. For
  example, apps have used it to parse a user's free-form input into
  structured **tasks and dates** ("Call Sophia Friday" becomes a
  scheduled call on
  Friday)[\[9\]](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/#:~:text=achieve%20their%20goals,add%20them%20directly%20to%20Stuff).
  By leveraging **specialized adapters** and prompts, you can enhance
  NLU for specific domains. Apple provides a *Content Tagging* adapter
  for first-class support of topic tagging, entity recognition, and
  intent
  detection[\[10\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=the%20content%20tagging%20adapter,to%20extract%20topics%20from%20it).
  This adapter, used via
  `SystemLanguageModel(useCase: .contentTagging)`, is fine-tuned for
  generating topic tags or other labels from text using the same
  on-device
  model[\[10\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=the%20content%20tagging%20adapter,to%20extract%20topics%20from%20it).
  You can still define a custom schema for the output (e.g. a struct of
  tags or entities) to get structured NLU results.

- **Guided Structured Output:** Use **Guided Generation** to ensure the
  model's output follows a specific structure or format. The framework
  introduces the `@Generable` macro to define Swift types (structs or
  enums) that represent the desired output
  schema[\[11\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=When%20you%20import%20FoundationModels%2C%20you,to%20generate%20an%20instance%20of).
  Mark all output fields as properties of a `@Generable` struct; these
  may include basic types (`String`, `Int`, `Bool`, etc.), arrays, or
  even nested generable types (including recursive
  types)[\[12\]\[13\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Generable%20types%20can%20be%20constructed,in%20domains%20like%20generative%20UIs).
  Optionally use the `@Guide` macro on properties to provide natural
  language descriptions or constrain acceptable values (e.g. range,
  format) for that
  field[\[14\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=generate%20an%20instance%20of).
  When you request a response **generating** a particular `@Generable`
  type, the framework employs constrained decoding to guarantee the
  model's reply can be parsed into that
  type[\[15\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20most%20important%20thing%20to,a%20technique%20called%20constrained%20decoding).
  This eliminates unreliable string parsing and ensures **structural
  correctness** of
  responses[\[16\]](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates#:~:text=highly%20optimized%2C%20complementary%20implementations%20of,by%20the%20Swift%20type%20system).
  You no longer need to prompt with "please output JSON"; the framework
  automatically formats the model output as JSON under the hood and
  decodes it into your Swift
  struct[\[17\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Observe%20how%20our%20prompt%20no,care%20of%20that%20for%20you)[\[18\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20most%20important%20part%2C%20of,map%20onto%20an%20engaging%20view).
  Focus your prompts on content and behavior rather than worrying about
  output syntax.

- **Tool Invocation (Tool Calling):** Extend the model's capabilities by
  defining **tools** -- custom functions in your app that the model can
  call
  autonomously[\[19\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=tool%20calling%21%20Thanks%20Erik%21%20Tool,it%E2%80%99s%20difficult%20to%20decide%20programmatically)[\[20\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Finally%2C%20it%20allows%20the%20model,or%20in%20the%20real%20world).
  Conform your tool types to the `Tool` protocol, which requires a
  unique `name` and a descriptive explanation of what the tool
  does[\[21\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Here%20we%E2%80%99re%20defining%20a%20simple,great%20way%20to%20get%20started).
  The framework will include this name and description in the model's
  context so it knows the tool is available and when to use
  it[\[22\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20protocol%20first%20requires%20you,language%20description%20of%20the%20tool).
  Implement the tool's `call(arguments:)` async method to perform the
  desired action or fetch data. **Tool arguments** must be a `Generable`
  type (defined via `@Generable struct`) because tool invocation is
  built on guided generation -- the model will only produce a tool call
  if it can generate valid arguments matching that
  schema[\[23\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20argument%20to%20the%20call,can%20be%20any%20Generable%20type).
  The framework ensures the model never emits an invalid tool name or
  malformed
  arguments[\[23\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20argument%20to%20the%20call,can%20be%20any%20Generable%20type).
  In the `call` method, use any APIs or services needed (e.g. query a
  database, call a web API, use a system framework like HealthKit or
  WeatherKit) to fulfill the request. Return the result as a
  `ToolOutput` -- this can be created from structured data (any
  `GeneratedContent` that matches a Generable schema) or from a plain
  string if the tool's output is
  narrative[\[24\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=After%20defining%20your%20arguments%20type%2C,model%20has%20access%20to%20it).
  **Attach tools to the session** at initialization (e.g.
  `LanguageModelSession(tools: [MyTool()])`) so the model is aware of
  them during that
  session[\[25\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=To%20do%20so%2C%20pass%20your,model%20for%20the%20session%E2%80%99s%20lifetime).
  The model will autonomously decide *if and when* to call a tool based
  on the user's prompt and the tool
  descriptions[\[26\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=model%20many%20additional%20capabilities,it%E2%80%99s%20difficult%20to%20decide%20programmatically)[\[27\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Now%2C%20if%20the%20model%20deems,%E2%80%94%20querying%20restaurants%20and%20hotels).
  When a tool is invoked, the framework executes your `call` method,
  injects the tool's output back into the conversation transcript, and
  then lets the model continue to generate its final answer with that
  additional
  information[\[27\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Now%2C%20if%20the%20model%20deems,%E2%80%94%20querying%20restaurants%20and%20hotels)[\[28\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=At%20this%20phase%2C%20the%20FoundationModels,to%20furnish%20the%20final%20response).
  Tool calling enables the model to fetch real-time data or perform
  actions beyond its built-in
  knowledge[\[29\]](https://www.appcoda.com/tool-calling/#:~:text=information%20about%20trending%20movies,related%20questions%20using%20live%20data)[\[30\]](https://www.appcoda.com/tool-calling/#:~:text=movie,information%20directly%20in%20the%20app),
  all while keeping the logic and data access under your app's control.

- **Streaming Responses:** For a more responsive UI, use the
  asynchronous streaming API (`session.streamResponse`) to receive
  partial results as the model generates
  them[\[31\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=The%20Session%20stream%20response)[\[32\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=for%20try%20await%20partial%20in,PartiallyGenerated%20updateUI%28with%3A%20partial%29).
  Instead of raw text tokens, the Foundation Models framework streams
  **snapshot objects** representing partially-filled `@Generable`
  outputs[\[33\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=Under%20the%20hood%2C%20Foundation%20Models,is%20such%20a%20snapshot)[\[34\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=When%20you%20use%C2%A0streamResponse,For%20example%2C%20if%20you%20have).
  Each interim snapshot has the same fields as your output type but with
  incomplete data (fields are `nil` until
  generated)[\[35\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=optional%2C%20reflecting%20incremental%20completion,example%2C%20if%20you%20have).
  By iterating over the AsyncSequence, you can update your SwiftUI views
  or UI elements progressively as each field in the structure becomes
  available[\[36\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=structured%20output,is%20such%20a%20snapshot)[\[37\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=Then%C2%A0,and%20gradually%20get%20values).
  This structured streaming avoids the need to manually concatenate
  tokens or parse incremental JSON, since you get well-typed partial
  objects. It's especially powerful for gradually displaying content
  like lists or multi-field data with smooth
  animations[\[38\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=You%20append%20each%20delta%20as,response%20grows%20as%20you%20do)[\[39\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=But%20it%20gets%20tricky%20when,when%20working%20with%20structured%20output).
  Remember that properties are generated in order; consider declaring
  important summary fields last to improve coherence and animation
  order[\[40\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=To%20wrap%20up%2C%20let%E2%80%99s%20review,some%20best%20practices%20for%20streaming).

- **Safety and Guardrails:** The on-device model has built-in guardrails
  to reduce harmful or unwanted
  outputs[\[41\]](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates#:~:text=Tool%20calling%20offers%20developers%20the,of%20information%20sources%20or%20services)[\[5\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=instructions%20will%20be%20used%20if,you%20don%E2%80%99t%20specify%20any).
  Handle errors such as `GenerationError.guardrailViolation` (triggered
  if content violates Apple's safety rules) by catching exceptions from
  `respond`/`streamResponse`. The model supports multiple languages (15+
  locales)[\[42\]](https://machinelearning.apple.com/research/apple-foundation-models-2025-updates#:~:text=features%20integrated%20across%20our%20platforms,silicon%2C%20and%20include%20a%20compact),
  but will return an error if asked to process an unsupported language
  or if Apple Intelligence is
  disabled/unavailable[\[3\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=emotions,availability%20property%20on%20the%20SystemLanguageModel).
  Always test your prompts and outputs, especially for sensitive
  content. Use developer instructions to enforce style or refusals in
  certain cases as needed. By keeping all AI processing on-device,
  Apple's framework inherently protects privacy (no user text or model
  prompts ever leave the
  device)[\[2\]](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/#:~:text=With%20the%20release%20of%20iOS,and%20help%20users%20in%20new).

# Workflow

1.  **Initialize Model Session:** Ensure the device and OS support the
    Foundation Model. Then create a `LanguageModelSession` (or
    `SystemLanguageModel`) instance. Optionally pass a custom
    `Instructions` object with system-level guidance for the model (e.g.
    role-playing as an expert, response
    style)[\[4\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=stateful%20sessions,you%20can%20provide%20custom%20instructions).
    Also provide any `Tool` instances via the session's initializer if
    your feature will use tool
    calling[\[25\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=To%20do%20so%2C%20pass%20your,model%20for%20the%20session%E2%80%99s%20lifetime).
    For specialized NLU tasks, you may initialize a
    `SystemLanguageModel` with a built-in adapter (e.g.
    `.contentTagging`) instead of the general
    model[\[10\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=the%20content%20tagging%20adapter,to%20extract%20topics%20from%20it).
    Check `SystemLanguageModel.availability` and only proceed if
    `.available`[\[3\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=emotions,availability%20property%20on%20the%20SystemLanguageModel).

2.  **Define Output Schema (Optional):** If you need structured output,
    declare Swift types to model the response. Use `@Generable` to
    annotate the type (for example, a struct with fields for the info
    you want). Add `@Guide` on any fields where you want to constrain
    the output format or provide hints (for instance,
    `@Guide(description: "ISO 8601 date string") var dueDate: String?`).
    The framework will auto-generate a JSON schema from your type at
    compile time and use it to guide the model's
    output[\[11\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=When%20you%20import%20FoundationModels%2C%20you,to%20generate%20an%20instance%20of)[\[15\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20most%20important%20thing%20to,a%20technique%20called%20constrained%20decoding).

3.  **Construct Prompt:** Formulate the user prompt or query. This can
    be a simple string or a `Prompt` object if you need to include
    variables or formatted text. Keep prompts focused on the
    task/content you want; avoid having to specify output format (the
    guided generation mechanism will handle
    that)[\[17\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Observe%20how%20our%20prompt%20no,care%20of%20that%20for%20you).
    If you provided custom instructions in the session, you generally do
    **not** need to include those again in the prompt; they are
    automatically prepended for each query.

4.  **Request Model Response:** Call the session's API to generate a
    response. There are two primary modes:

5.  **Synchronous generation:** Use
    `try await session.respond(to: prompt, generating: OutputType.self)`
    to get a complete `Response<OutputType>` in one
    call[\[43\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=The%20parameters%20of%20a%C2%A0,include)[\[44\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=The%20method%20returns%20a%C2%A0Response%C2%A0object.%20The%C2%A0,of%20user%20and%20assistant%20messages).
    If you don't need structured output, you can omit the `generating:`
    parameter and get a `Response<String>` containing the model's reply
    text. You can also pass `GenerationOptions` to adjust parameters
    like temperature (creativity), max tokens, or sampling
    method[\[45\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=,the%20maximum%20number%20of%20tokens)[\[46\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=let%20options%20%3D%20GenerationOptions,8%2C%20maximumResponseTokens%3A%20200).
    The first call may incur a short delay as the model warms up; you
    can call a lightweight method (e.g. `session.prewarm()`) in advance
    if needed.

6.  **Streaming generation:** Use
    `session.streamResponse(generating: OutputType.self) { prompt }` to
    get an `AsyncSequence` of partial
    results[\[31\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=The%20Session%20stream%20response).
    Iterate over the sequence with `for await` to handle each
    `Partial<OutputType>` snapshot as it
    arrives[\[47\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=for%20try%20await%20partial%20in,PartiallyGenerated%20updateUI%28with%3A%20partial%29).
    Update your UI or state with each partial (`partial.content` will be
    a partially-filled instance of your struct). Continue until the
    sequence completes, then use the final snapshot as the full result.
    Streaming is useful for long responses or when you want to show
    incremental progress (e.g. revealing parts of an answer one by
    one)[\[33\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=Under%20the%20hood%2C%20Foundation%20Models,is%20such%20a%20snapshot).

7.  **Process the Response:** Once `respond()` returns (or the stream
    completes), retrieve the output:

8.  For a structured response, you'll get a `Response<T>` where `T` is
    your Generable type. Access `response.content` to get the fully
    decoded Swift struct (already populated with the model's
    output)[\[44\]](https://www.createwithswift.com/exploring-the-foundation-models-framework/#:~:text=The%20method%20returns%20a%C2%A0Response%C2%A0object.%20The%C2%A0,of%20user%20and%20assistant%20messages).
    You can then use this object directly in your app (e.g. update the
    UI with these values, or pass it to other logic). The `Response`
    also contains a `transcriptEntries` property if you need to examine
    the conversation history or the raw text form.

9.  For a text response (`Response<String>`), simply use the `.content`
    string. For example, display it in a text view or speak it with
    AVSpeechSynthesizer.

10. If the model invoked any tools during processing, their effects
    should be reflected in the final content. For instance, if a tool
    fetched data, the answer will include that data. The tool call and
    its output are also logged as entries in the session transcript (you
    can inspect `session.transcript` to see tool invocations and results
    in
    sequence)[\[48\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=On%20the%20left%20we%20have,destination%20we%20want%20to%20visit)[\[28\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=At%20this%20phase%2C%20the%20FoundationModels,to%20furnish%20the%20final%20response).

11. **Handle Errors and Completion:** Be prepared to catch errors from
    the `respond` call. For example, a `guardrailViolation` error
    indicates the input or requested content violated a safety rule (the
    model refused), in which case you might show an error message or a
    sanitized response. An `unavailable` error indicates the model
    couldn't run (perhaps the device is not in a supported region or
    Apple Intelligence is
    off)[\[3\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=emotions,availability%20property%20on%20the%20SystemLanguageModel).
    Also, after each interaction, `session.isResponding` will go back to
    `false` -- at this point it's safe to allow the user to submit
    another prompt or end the session.

12. **Iterate or End Session:** If your feature involves multiple
    back-and-forth turns, you can continue calling `respond()` on the
    same session object to leverage the accumulated
    context[\[7\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Now%20that%20you%20have%20initialized,back%20to%20writing%20a%20haiku).
    The model will remember prior prompts and its answers, enabling
    follow-up questions or refinements (e.g. "Now do the same for Paris"
    referring to a previous travel itinerary). If instead each usage is
    independent, you might reset or discard the session after use.
    (Currently there's no explicit "reset" method, but you can simply
    create a new session for a fresh context.)

13. **Optimize & Refine:** Once basic integration works, refine your
    prompts, instructions, and tools for better results. Use developer
    tools like the **Foundation Models Debugger/Instrument** to profile
    token usage, response time, and verify schema adherence. Ensure your
    `@Generable` schema aligns with what the model can produce (complex
    schemas may require guiding instructions or breaking tasks into
    smaller prompts). Leverage the model's strengths in language
    understanding but provide tools or heuristics for tasks it isn't
    reliable at (e.g. real-time info lookup, calculations, highly
    domain-specific
    answers)[\[49\]](https://www.appcoda.com/tool-calling/#:~:text=The%20on,app%27s%20functions%20or%20external%20APIs)[\[30\]](https://www.appcoda.com/tool-calling/#:~:text=movie,information%20directly%20in%20the%20app).
    Test in different conditions (device types, languages, content
    scenarios) to validate the on-device model's performance.

# Examples

- **Structured Output Example:** Suppose you want the model to generate
  a question-and-answer pair for a trivia app. First, define a Swift
  struct with the desired fields:

<!-- -->

- import FoundationModels
      @Generable struct QuizQA: Equatable {
          let question: String
          let answer: String
      }

  Now you can prompt the model and get a `QuizQA` result:

      let session = LanguageModelSession()
      let userPrompt = "Generate a trivia question about WWDC and provide the answer."
      let result: Response<QuizQA> = try await session.respond(to: userPrompt, generating: QuizQA.self)
      let qa = result.content   // QuizQA object with `question` and `answer` filled in.
      print("Q: \(qa.question)\nA: \(qa.answer)")

  The Foundation Models framework ensures the response is a JSON that
  matches `QuizQA` and parses it accordingly -- for example, it might
  return *question*: "What does WWDC stand for?" and *answer*:
  "Worldwide Developers Conference." (Your actual output will vary, but
  it will always conform to the `QuizQA`
  structure)[\[18\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20most%20important%20part%2C%20of,map%20onto%20an%20engaging%20view)[\[15\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=The%20most%20important%20thing%20to,a%20technique%20called%20constrained%20decoding).

<!-- -->

- **Tool Invocation Example:** Consider an app that needs current
  weather info. You can define a tool that calls WeatherKit:

<!-- -->

- struct WeatherTool: Tool {
          let name = "getWeather"
          let description = "Look up the current temperature for a city."
          @Generable struct Arguments { let city: String }
          func call(arguments: Arguments) async throws -> ToolOutput {
              // Use WeatherKit or an API to get weather for arguments.city
              let (temp, condition) = try await fetchWeather(for: arguments.city)
              let reply = "It is \(temp)° and \(condition) now in \(arguments.city)."
              return ToolOutput(reply)
          }
      }

  When initializing the session, attach this tool:

      let session = LanguageModelSession(tools: [WeatherTool()])

  Now if the user prompt is *"What's the weather in* *Cupertino* *right
  now?"*, the model can decide to invoke `WeatherTool` internally to get
  live data. It will produce a **tool call** like
  `getWeather(city: "Cupertino")` behind the
  scenes[\[50\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=Now%2C%20if%20the%20model%20deems,%E2%80%94%20querying%20restaurants%20and%20hotels),
  causing your `WeatherTool.call` to run. The tool's output (e.g. *"It
  is 72° and sunny now in Cupertino."*) is then inserted into the
  model's context, and the model uses it to complete the final
  answer[\[28\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=At%20this%20phase%2C%20the%20FoundationModels,to%20furnish%20the%20final%20response)[\[51\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=temperature%20of%20a%20given%20city,model%20has%20access%20to%20it).
  The user ultimately sees a response that includes the real weather
  info, even though the base model by itself didn't know it. This
  demonstrates how tool calling can **augment the on-device model** with
  up-to-date information and
  actions[\[29\]](https://www.appcoda.com/tool-calling/#:~:text=information%20about%20trending%20movies,related%20questions%20using%20live%20data)[\[30\]](https://www.appcoda.com/tool-calling/#:~:text=movie,information%20directly%20in%20the%20app).

<!-- -->

- **NLU Tagging Example:** You can use the content tagging adapter to
  extract topics or keywords from text. For instance:

<!-- -->

- @Generable struct Topics { let topics: [String] }
      let session = SystemLanguageModel(useCase: .contentTagging)
      let text = "Apple unveiled new AR features in iOS at WWDC."
      let tags: Topics = try await session.respond(to: text, generating: Topics.self).content
      print(tags.topics)  // e.g. ["Apple", "AR", "iOS", "WWDC"]

  Here the model categorizes the input sentence, identifying key topics
  or entities. Under the hood, the `.contentTagging` adapter uses a
  fine-tuned model head to improve accuracy for tagging
  tasks[\[10\]](https://developer.apple.com/videos/play/wwdc2025/286/#:~:text=the%20content%20tagging%20adapter,to%20extract%20topics%20from%20it).
  We still leverage guided generation to output a consistent JSON with
  an array of topics. This way, the app can display or use these tags
  (for example, to index content or trigger certain features) without
  any server calls. All processing is local, and sensitive text never
  leaves the
  device[\[2\]](https://www.apple.com/newsroom/2025/09/apples-foundation-models-framework-unlocks-new-intelligent-app-experiences/#:~:text=With%20the%20release%20of%20iOS,and%20help%20users%20in%20new).

