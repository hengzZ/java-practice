# Java 配置
—— Java 注解配置

示例：
```java
package cn.demo.config;

@Configuration
public class JdbcConfig {
    @Bean
    public DataSource dataSource() {
        DruidDataSource dataSource = new DruidDataSource();
        dataSource.setDriverClassName("");
        dataSource.setUrl("");
        dataSource.setUsername("");
        dataSource.setPassword("");
        return dataSource;
    }
}
```
