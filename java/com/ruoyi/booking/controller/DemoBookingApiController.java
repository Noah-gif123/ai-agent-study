package com.ruoyi.booking.controller;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import com.ruoyi.common.annotation.Anonymous;
import com.ruoyi.common.core.controller.BaseController;
import com.ruoyi.common.core.domain.AjaxResult;
import com.ruoyi.system.domain.DemoBooth;
import com.ruoyi.system.domain.DemoBooking;
import com.ruoyi.system.service.IDemoBoothService;
import com.ruoyi.system.service.IDemoBookingService;

/**
 * 展位预约前端API Controller（匿名访问）
 * 供门户前端 AI 助手调用
 *
 * @author ruoyi
 * @date 2026-06-30
 */
@Anonymous
@RestController
@RequestMapping("/api/booking")
public class DemoBookingApiController extends BaseController {

    @Autowired
    private IDemoBookingService demoBookingService;

    @Autowired
    private IDemoBoothService demoBoothService;

    /**
     * 提交展位预约（匿名访问，供门户前端 AI 助手调用）
     */
    @PostMapping("/submit")
    public AjaxResult submit(@RequestBody Map<String, Object> params) {
        String boothName = (String) params.getOrDefault("boothName", "");
        String boothType = (String) params.getOrDefault("boothType", "标准展位");
        String userName = (String) params.getOrDefault("userName", "");
        String email = (String) params.getOrDefault("email", "");
        String phone = (String) params.getOrDefault("phone", "");
        String bookingDateStr = (String) params.getOrDefault("bookingDate", "");
        String remark = (String) params.getOrDefault("remark", "");
        Object quantityObj = params.get("quantity");
        Long quantity = 1L;
        if (quantityObj instanceof Number) {
            quantity = ((Number) quantityObj).longValue();
        }

        // 参数校验
        if (userName.isBlank()) {
            return AjaxResult.error("请填写您的姓名");
        }
        if (phone.isBlank()) {
            return AjaxResult.error("请填写您的联系电话");
        }
        if (email.isBlank() && phone.isBlank()) {
            return AjaxResult.error("请至少填写邮箱或电话，方便我们联系您");
        }

        // 预约日期解析
        Date bookingDate = null;
        if (!bookingDateStr.isBlank()) {
            try {
                SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
                bookingDate = sdf.parse(bookingDateStr);
            } catch (ParseException e) {
                return AjaxResult.error("预约日期格式不正确，请使用 yyyy-MM-dd 格式");
            }
        }

        // 查找展位：根据展位名称和类型匹配
        DemoBooth queryParam = new DemoBooth();
        queryParam.setBoothName(boothName);
        if (boothType.contains("标准")) {
            queryParam.setBoothType("0");
        } else if (boothType.contains("特装")) {
            queryParam.setBoothType("1");
        }
        List<DemoBooth> boothList = demoBoothService.selectDemoBoothList(queryParam);

        Long boothId = null;
        if (boothList != null && !boothList.isEmpty()) {
            boothId = boothList.get(0).getBoothId();
        }

        // 创建预约记录
        DemoBooking booking = new DemoBooking();
        booking.setBoothId(boothId);
        booking.setUserName(userName);
        booking.setEmai(email);
        booking.setPhonenumber(phone);
        booking.setBookingQuantity(quantity);
        booking.setBookingDate(bookingDate);
        booking.setBookingStatus("SUBMITTED");
        booking.setCreateTime(new Date());
        if (!remark.isBlank()) {
            booking.setRemark(remark);
        }

        int rows = demoBookingService.insertDemoBooking(booking);
        if (rows > 0) {
            Map<String, Object> data = new HashMap<>();
            data.put("bookingId", booking.getBookingId());
            data.put("message", "预约成功！我们会尽快与您联系确认展位信息。");
            return AjaxResult.success("预约成功！我们会尽快与您联系确认展位信息。", data);
        } else {
            return AjaxResult.error("预约提交失败，请稍后重试");
        }
    }

    /**
     * 获取可预约的展位选项列表（匿名访问，供前端下拉选择）
     */
    @GetMapping("/boothOptions")
    public AjaxResult boothOptions() {
        DemoBooth queryParam = new DemoBooth();
        List<DemoBooth> boothList = demoBoothService.selectDemoBoothList(queryParam);

        List<Map<String, Object>> options = boothList.stream().map(booth -> {
            Map<String, Object> item = new HashMap<>();
            item.put("boothName", booth.getBoothName());
            item.put("boothType", "0".equals(booth.getBoothType()) ? "标准展位" : "特装展位");
            item.put("boothTypeCode", booth.getBoothType());
            item.put("availableQuantity", booth.getAvailableQuantity());
            return item;
        }).collect(java.util.stream.Collectors.toList());

        return AjaxResult.success(options);
    }

    /**
     * 查询用户的预约记录（匿名访问，根据手机号或邮箱查询）
     */
    @GetMapping("/myBookings")
    public AjaxResult myBookings(
            @RequestParam(required = false) String phone,
            @RequestParam(required = false) String email) {

        if ((phone == null || phone.isBlank()) && (email == null || email.isBlank())) {
            return AjaxResult.error("请提供手机号或邮箱以查询预约记录");
        }

        DemoBooking queryParam = new DemoBooking();
        if (phone != null && !phone.isBlank()) {
            queryParam.setPhonenumber(phone.trim());
        }
        if (email != null && !email.isBlank()) {
            queryParam.setEmai(email.trim());
        }

        List<DemoBooking> list = demoBookingService.selectDemoBookingList(queryParam);

        // 构建返回数据，包含展位信息映射
        List<Map<String, Object>> resultList = list.stream().map(b -> {
            Map<String, Object> item = new HashMap<>();
            item.put("bookingId", b.getBookingId());
            item.put("userName", b.getUserName());
            item.put("email", b.getEmai());
            item.put("phone", b.getPhonenumber());
            item.put("bookingQuantity", b.getBookingQuantity());
            item.put("bookingDate", b.getBookingDate());
            item.put("bookingStatus", b.getBookingStatus());
            item.put("remark", b.getRemark());
            item.put("createTime", b.getCreateTime());
            // 查询展位信息
            if (b.getBoothId() != null) {
                DemoBooth booth = demoBoothService.selectDemoBoothByBoothId(b.getBoothId());
                if (booth != null) {
                    item.put("boothName", booth.getBoothName());
                    item.put("boothType", "0".equals(booth.getBoothType()) ? "标准展位" : "特装展位");
                }
            }
            return item;
        }).collect(java.util.stream.Collectors.toList());

        Map<String, Object> data = new HashMap<>();
        data.put("total", resultList.size());
        data.put("list", resultList);
        return AjaxResult.success(data);
    }
}
