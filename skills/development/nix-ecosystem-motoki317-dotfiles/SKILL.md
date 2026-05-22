---
name: Nix Ecosystem
description: This skill should be used when the user asks to "write nix", "nix expression", "flake.nix", "home-manager config", "programs.*", "services.*", or works with Nix language, flakes, or Home Manager. Provides comprehensive Nix ecosystem patterns and best practices.
---

<purpose>
  Provide comprehensive patterns for Nix language, flakes, and Home Manager configuration.
</purpose>

<nix_language>
  <fundamentals>
    <concept name="lazy_evaluation">
      <description>Nix is lazily evaluated. Expressions are only computed when needed.</description>
      <example>
        <note>Only evaluates needed attributes</note>
        let
        expensive = builtins.trace "Computing expensive" (1 + 1);
        in
        { a = 1; b = expensive; }.a # Does not compute expensive
      </example>
    </concept>

    <concept name="pure_functions">
      <description>All Nix functions are pure. Same inputs always produce same outputs.</description>
      <example>
        <note>Pure function - always returns same result for same input</note>
        double = x: x * 2;

        <note>Avoid side effects; use derivations for build actions</note>
        buildResult = pkgs.stdenv.mkDerivation { ... };
      </example>
    </concept>

    <concept name="attribute_sets">
      <description>Primary data structure in Nix</description>
      <example>
        <note>Basic attribute set</note>
        { attr1 = value1; attr2 = value2; }

        <note>Access patterns</note>
        set.attr
        set."attr-with-dashes"

        <note>Recursive attribute set</note>
        rec { a = 1; b = a + 1; }
      </example>
    </concept>
  </fundamentals>

  <patterns>
    <pattern name="let_in">
      <description>Local bindings for complex expressions</description>
      <example>
        let
        helper = x: x + 1;
        value = helper 5;
        in
        value * 2
      </example>
    </pattern>

    <pattern name="with">
      <description>Bring attribute set into scope</description>
      <example>
        with pkgs; [ git vim tmux ]
      </example>
      <warning>Avoid nested with; prefer explicit references for clarity</warning>
    </pattern>

    <pattern name="inherit">
      <description>Copy attributes from another set</description>
      <example>
        { inherit (pkgs) git vim; inherit name version; }
      </example>
    </pattern>

    <pattern name="overlay">
      <description>Modify or extend nixpkgs</description>
      <example>
        final: prev: {
        myPackage = prev.myPackage.override { ... };
        }
      </example>
      <decision_tree name="when_to_use">
        <question>Do you need to modify existing packages or add new ones globally?</question>
        <if_yes>Use overlays to extend nixpkgs</if_yes>
        <if_no>Use local package definitions with callPackage</if_no>
      </decision_tree>
    </pattern>

    <pattern name="callPackage">
      <description>Dependency injection pattern</description>
      <example>
        myPackage = pkgs.callPackage ./package.nix { };
      </example>
    </pattern>

    <pattern name="mkDerivation">
      <description>Standard package builder</description>
      <example>
        pkgs.stdenv.mkDerivation {
        pname = "mypackage";
        version = "1.0.0";
        src = fetchFromGitHub { ... };

        nativeBuildInputs = [ pkgs.cmake ];
        buildInputs = [ pkgs.openssl ];

        installPhase = ''
        mkdir -p $out/bin
        cp mypackage $out/bin/
        '';
        }
      </example>
      <note>Required attributes: pname, version, src</note>
      <note>Standard phases: unpackPhase, patchPhase, configurePhase, buildPhase, installPhase</note>
    </pattern>

    <pattern name="build_inputs">
      <description>Dependency specification in derivations</description>
      <example>
        {
        # Tools run at build time (compilers, build tools)
        nativeBuildInputs = [ cmake pkg-config ];

        # Libraries linked at runtime
        buildInputs = [ openssl zlib ];
        }
      </example>
    </pattern>

    <pattern name="options_config">
      <description>NixOS/Home Manager module structure</description>
      <example>
        { config, lib, pkgs, ... }:
        {
        options.myModule = {
        enable = lib.mkEnableOption "my module";
        setting = lib.mkOption {
        type = lib.types.str;
        default = "value";
        description = "A setting";
        };
        };

        config = lib.mkIf config.myModule.enable { # configuration when enabled
        };
        }
      </example>
    </pattern>

    <pattern name="mkOption">
      <description>Define module options with types and defaults</description>
      <example>
        options.myOption = lib.mkOption {
        type = lib.types.bool;
        default = false;
        description = "Enable my feature";
        example = true;
        };
      </example>
      <note>Common types: lib.types.bool, lib.types.str, lib.types.listOf, lib.types.attrsOf</note>
    </pattern>

    <pattern name="mkEnableOption">
      <description>Shorthand for boolean enable option</description>
      <example>
        enable = lib.mkEnableOption "my service";
      </example>
    </pattern>
  </patterns>

  <anti_patterns>
    <avoid name="impure_paths">
      <description>Directly referencing absolute paths breaks reproducibility</description>
      <instead>Use fetchurl, fetchFromGitHub, or relative paths within the repository</instead>
    </avoid>

    <avoid name="nested_with">
      <description>Multiple nested with statements reduce code clarity</description>
      <instead>Prefer explicit attribute access (pkgs.git) for better readability</instead>
    </avoid>

    <avoid name="rec_overuse">
      <description>Recursive attribute sets can be hard to understand and maintain</description>
      <instead>Use let-in for complex recursive definitions</instead>
    </avoid>

    <avoid name="string_interpolation_abuse">
      <description>Using string interpolation for path operations is error-prone</description>
      <instead>Use lib functions for path manipulation (lib.concatStringsSep, builtins.path)</instead>
    </avoid>
  </anti_patterns>
</nix_language>

<flakes>
  <concept name="flake_structure">
    <description>Basic structure of a flake.nix file</description>
    <example>
      {
      description = "Project description";

      inputs = {
      nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
      };

      outputs = { self, nixpkgs, ... }@inputs: { # output attributes
      };
      }
    </example>
  </concept>

  <outputs>
    <concept name="packages">
      <description>Derivations for nix build</description>
      <example>
        packages.x86_64-linux.default = pkgs.hello;
      </example>
    </concept>

    <concept name="devShells">
      <description>Development environments for nix develop</description>
      <example>
        devShells.x86_64-linux.default = pkgs.mkShell {
        packages = [ pkgs.nodejs ];
        };
      </example>
    </concept>

    <concept name="apps">
      <description>Runnable applications for nix run</description>
      <example>
        apps.x86_64-linux.default = {
        type = "app";
        program = "${pkgs.hello}/bin/hello";
        };
      </example>
    </concept>

    <concept name="overlays">
      <description>Nixpkgs overlays</description>
      <example>
        overlays.default = final: prev: {
        myPackage = prev.callPackage ./myPackage.nix { };
        };
      </example>
    </concept>

    <concept name="nixosModules">
      <description>NixOS modules</description>
      <example>
        nixosModules.default = { config, lib, pkgs, ... }: {
        options.services.myService = { ... };
        config = { ... };
        };
      </example>
    </concept>

    <concept name="homeManagerModules">
      <description>Home Manager modules</description>
      <example>
        homeManagerModules.default = { config, lib, pkgs, ... }: {
        options.programs.myProgram = { ... };
        config = { ... };
        };
      </example>
    </concept>

    <concept name="nixosConfigurations">
      <description>Full NixOS system configurations</description>
      <example>
        nixosConfigurations.hostname = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [ ./configuration.nix ];
        };
      </example>
    </concept>

    <concept name="homeConfigurations">
      <description>Home Manager configurations</description>
      <example>
        homeConfigurations."user@host" = home-manager.lib.homeManagerConfiguration {
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
        modules = [ ./home.nix ];
        };
      </example>
    </concept>
  </outputs>

  <patterns>
    <pattern name="github_input">
      <description>Reference GitHub repositories as flake inputs</description>
      <example>
        inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
        # Specific branch
        stable.url = "github:NixOS/nixpkgs/nixos-24.11";
        # Specific revision
        pinned.url = "github:owner/repo/abc123def";
        };
      </example>
    </pattern>

    <pattern name="follows">
      <description>Share input between flakes to avoid duplication</description>
      <example>
        home-manager = {
        url = "github:nix-community/home-manager";
        inputs.nixpkgs.follows = "nixpkgs";
        };
      </example>
    </pattern>

    <pattern name="flake_false">
      <description>Non-flake inputs for legacy repositories</description>
      <example>
        my-source = {
        url = "github:owner/repo";
        flake = false;
        };
      </example>
    </pattern>

    <pattern name="per_system">
      <description>Generate outputs for multiple systems</description>
      <example>
        outputs = { self, nixpkgs, ... }:
        let
        systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
        forAllSystems = nixpkgs.lib.genAttrs systems;
        in {
        packages = forAllSystems (system:
        let pkgs = nixpkgs.legacyPackages.${system};
        in { default = pkgs.hello; }
        );
        };
      </example>
      <decision_tree name="when_to_use">
        <question>Does your flake need to support multiple platforms?</question>
        <if_yes>Use per-system pattern with genAttrs or flake-utils</if_yes>
        <if_no>Define outputs for single system directly</if_no>
      </decision_tree>
    </pattern>

    <pattern name="devShell">
      <description>Development environment with packages and hooks</description>
      <example>
        devShells.default = pkgs.mkShell {
        packages = with pkgs; [ nodejs yarn ];
        shellHook = ''
        echo "Development environment ready"
        '';
        };
      </example>
    </pattern>
  </patterns>

  <tools>
    <tool name="nix flake update">
      <description>Update all inputs to their latest versions</description>
      <use_case>Regular dependency updates</use_case>
    </tool>

    <tool name="nix flake update input-name">
      <description>Update a specific input</description>
      <use_case>Selective updates to test compatibility</use_case>
    </tool>

    <tool name="nix flake show">
      <description>Display all flake outputs</description>
      <use_case>Exploring available packages and configurations</use_case>
    </tool>

    <tool name="nix flake check">
      <description>Validate flake and run checks</description>
      <use_case>CI/CD validation, pre-commit checks</use_case>
    </tool>
  </tools>
</flakes>

<home_manager>
  <concept name="module_structure">
    <description>Standard Home Manager module structure</description>
    <example>
      { config, pkgs, lib, ... }:
      {
      options.custom.feature = {
      enable = lib.mkEnableOption "feature description";
      };

      config = lib.mkIf config.custom.feature.enable { # configuration when enabled
      };
      }
    </example>
  </concept>

  <patterns>
    <pattern name="by_program">
      <description>Organize modules by program name</description>
      <example>
        home-manager/programs/git.nix
        home-manager/programs/neovim.nix
        home-manager/programs/tmux.nix
      </example>
    </pattern>

    <pattern name="by_category">
      <description>Organize modules by category</description>
      <example>
        home-manager/development/default.nix
        home-manager/shell/default.nix
        home-manager/editors/default.nix
      </example>
    </pattern>

    <pattern name="imports">
      <description>Import multiple modules</description>
      <example>
        imports = [
        ./programs/git.nix
        ./programs/neovim.nix
        ./shell/fish.nix
        ];
      </example>
    </pattern>

    <pattern name="basic_enable">
      <description>Enable a program with defaults</description>
      <example>
        programs.git.enable = true;
      </example>
    </pattern>

    <pattern name="with_options">
      <description>Enable and configure a program</description>
      <example>
        programs.git = {
        enable = true;
        userName = "name";
        userEmail = "email";
        extraConfig = {
        core.editor = "nvim";
        init.defaultBranch = "main";
        };
        };
      </example>
      <decision_tree name="when_to_use">
        <question>Does Home Manager provide built-in module for this program?</question>
        <if_yes>Use programs.* with configuration options</if_yes>
        <if_no>Use home.file or xdg.configFile for manual configuration</if_no>
      </decision_tree>
    </pattern>

    <pattern name="package_override">
      <description>Use alternative package version</description>
      <example>
        programs.git = {
        enable = true;
        package = pkgs.gitFull;
        };
      </example>
    </pattern>

    <pattern name="home.file">
      <description>Manage dotfiles directly</description>
      <example>
        home.file.".config/app/config" = {
        source = ./config;
        # or
        text = ''
        key = value
        '';
        };
      </example>
    </pattern>

    <pattern name="xdg.configFile">
      <description>XDG config directory files</description>
      <example>
        xdg.configFile."app/config".source = ./config;
      </example>
    </pattern>

    <pattern name="home.sessionVariables">
      <description>Environment variables for login shells</description>
      <example>
        home.sessionVariables = {
        EDITOR = "nvim";
        PAGER = "less";
        };
      </example>
    </pattern>

    <pattern name="home.sessionPath">
      <description>Add directories to PATH</description>
      <example>
        home.sessionPath = [ "$HOME/.local/bin" ];
      </example>
    </pattern>
  </patterns>

  <common_modules>
    <concept name="programs.git">
      <description>Git version control configuration</description>
      <example>
        programs.git = {
        enable = true;
        userName = "Your Name";
        userEmail = "email@example.com";
        signing = {
        key = "KEY_ID";
        signByDefault = true;
        };
        aliases = {
        co = "checkout";
        st = "status";
        };
        extraConfig = {
        core.editor = "nvim";
        };
        };
      </example>
    </concept>

    <concept name="programs.neovim">
      <description>Neovim editor configuration</description>
      <example>
        programs.neovim = {
        enable = true;
        viAlias = true;
        vimAlias = true;
        plugins = with pkgs.vimPlugins; [
        vim-commentary
        vim-surround
        ];
        extraConfig = ''
        set number
        set relativenumber
        '';
        extraLuaConfig = ''
        vim.opt.expandtab = true
        '';
        };
      </example>
    </concept>

    <concept name="programs.fish">
      <description>Fish shell configuration</description>
      <example>
        programs.fish = {
        enable = true;
        shellInit = ''
        set -g fish_greeting
        '';
        shellAliases = {
        ll = "ls -lah";
        };
        functions = {
        gitignore = "curl -sL https://www.gitignore.io/api/$argv";
        };
        plugins = [
        { name = "z"; src = pkgs.fishPlugins.z.src; }
        ];
        };
      </example>
    </concept>

    <concept name="programs.tmux">
      <description>Terminal multiplexer configuration</description>
      <example>
        programs.tmux = {
        enable = true;
        terminal = "screen-256color";
        keyMode = "vi";
        plugins = with pkgs.tmuxPlugins; [
        sensible
        yank
        ];
        extraConfig = ''
        set -g mouse on
        '';
        };
      </example>
    </concept>

    <concept name="programs.direnv">
      <description>Directory-specific environment loader</description>
      <example>
        programs.direnv = {
        enable = true;
        nix-direnv.enable = true;
        enableBashIntegration = true;
        enableZshIntegration = true;
        };
      </example>
    </concept>
  </common_modules>

  <best_practices>
    <practice priority="critical">
      Use programs.* when available instead of manual configuration
    </practice>

    <practice priority="critical">
      Set home.stateVersion to your initial HM version and do not change after initial setup unless migrating
    </practice>

    <practice priority="high">
      Group related configurations in separate modules for maintainability
    </practice>

    <practice priority="high">
      Use lib.mkIf for conditional configuration
    </practice>

    <practice priority="medium">
      Prefer xdg.configFile over home.file for XDG-compliant apps
    </practice>

    <practice priority="medium">
      Use home.packages for additional packages not configured via programs.*
    </practice>
  </best_practices>

  <concept name="state_version">
    <description>Track Home Manager state version for compatibility</description>
    <example>
      home.stateVersion = "24.11"; # Current stable. 25.05 (upcoming).
    </example>
    <warning>Do not change after initial setup unless migrating</warning>
  </concept>

  <concept name="minimal_mode">
    <description>HM 24.11+ (25.05 upcoming) supports minimal mode for faster evaluation</description>
    <example>
      imports = [
      "${modulesPath}/programs/fzf.nix"
      ];
    </example>
    <note>Advanced users optimizing evaluation time</note>
  </concept>
</home_manager>

<workflow>
  <phase name="analyze">
    <objective>Understand Nix expression requirements</objective>
    <step>1. Identify target: flake, module, derivation, or expression</step>
    <step>2. Check existing patterns in project</step>
    <step>3. Consult Serena memories for conventions</step>
  </phase>
  <phase name="implement">
    <objective>Write idiomatic Nix code</objective>
    <step>1. Follow patterns from decision trees</step>
    <step>2. Use appropriate lib functions</step>
    <step>3. Apply best practices for target type</step>
  </phase>
  <phase name="validate">
    <objective>Verify Nix expression correctness</objective>
    <step>1. Check syntax with nix flake check</step>
    <step>2. Verify evaluation with nix eval</step>
    <step>3. Test build with nix build</step>
  </phase>
</workflow>

<error_escalation>
  <level severity="low">
    <example>Style inconsistency in Nix expression</example>
    <action>Note issue, suggest formatting</action>
  </level>
  <level severity="medium">
    <example>Evaluation error or type mismatch</example>
    <action>Debug with --show-trace, fix expression</action>
  </level>
  <level severity="high">
    <example>Build failure in derivation</example>
    <action>Analyze build log, present options to user</action>
  </level>
  <level severity="critical">
    <example>Impure expression breaking reproducibility</example>
    <action>Block operation, require pure alternatives</action>
  </level>
</error_escalation>

<constraints>
  <must>Use lib functions for complex operations</must>
  <must>Follow project's existing Nix patterns</must>
  <must>Maintain reproducibility in all expressions</must>
  <avoid>Impure paths and absolute references</avoid>
  <avoid>Nested with statements</avoid>
  <avoid>Overusing rec for attribute sets</avoid>
</constraints>

<related_agents>
  <agent name="design">Architecture and module dependency analysis for Nix configurations</agent>
  <agent name="execute">Implementation of flake outputs, Home Manager modules, and NixOS configurations</agent>
  <agent name="code-quality">Nix expression validation, formatting, and best practices enforcement</agent>
</related_agents>

<related_skills>
  <skill name="serena-usage">Symbol operations for navigating Nix expressions and module definitions</skill>
  <skill name="context7-usage">Fetch latest nixpkgs and Home Manager documentation</skill>
  <skill name="investigation-patterns">Debug evaluation errors and understand derivation failures</skill>
</related_skills>

<nixos>
  <patterns>
    <pattern name="basic">
      <description>Basic NixOS configuration with Home Manager</description>
      <example>
        nixosConfigurations.hostname = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
        ./configuration.nix
        home-manager.nixosModules.home-manager
        ];
        specialArgs = { inherit inputs; };
        };
      </example>
    </pattern>

    <pattern name="standalone_home_manager">
      <description>Standalone Home Manager without NixOS</description>
      <example>
        homeConfigurations."user@host" = home-manager.lib.homeManagerConfiguration {
        pkgs = nixpkgs.legacyPackages.x86_64-linux;
        modules = [ ./home.nix ];
        extraSpecialArgs = { inherit inputs; };
        };
      </example>
    </pattern>

    <pattern name="as_nixos_module">
      <description>Home Manager as a NixOS module</description>
      <example>
        {
        imports = [ home-manager.nixosModules.home-manager ];

        home-manager.useGlobalPkgs = true;
        home-manager.useUserPackages = true;
        home-manager.users.username = import ./home.nix;
        }
      </example>
    </pattern>
  </patterns>
</nixos>
